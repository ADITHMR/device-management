const Project = require("../model/project.model");
const ProjectFile = require("../model/project-files.model");
const UserProjectAcquisition = require("../model/user-project-acquisition.model");
const Device = require("../model/user-device.model");
const { Sequelize } = require("sequelize");
const sequelize = require("../config/sequelize");
const path = require("path");

class ProjectService {
  async createProject(req, res) {
    try {
      const userId = req.user.id;

      if (!req.body.name) {
        return res.status(400).json({ error: "Project name is required" });
      }

      const projectData = {
        name: req.body.name,
        description: req.body.description,
        youtubeLink: req.body.youtubeLink,
        projectType: req.body.projectType || "free",
        maxAcquisitions: req.body.maxAcquisitions || 5,
        lastUpdated: new Date(),
      };

      // Handle image file
      if (req.files && req.files.image && req.files.image[0]) {
        projectData.imageUrl = `/images/projects/${req.files.image[0].filename}`;
      }

      const project = await Project.create({
        ...projectData,
        version: 1,
        userId,
      });

      if (req.files && req.files.length > 0) {
        const projectFilesData = req.files.map((file) => {
          if (file.isExtracted && file.extractPath) {
            return {
              projectId: project.id,
              filename: path.basename(file.originalname, ".zip"),
              fileType: "directory",
              fileSize: file.size,
              filePath: file.extractPath,
              mimetype: "application/directory",
              isZipExtracted: true,
              originalZipName: file.originalname,
            };
          } else {
            return {
              projectId: project.id,
              filename: file.filename,
              fileType: path.extname(file.originalname),
              fileSize: file.size,
              filePath: file.path,
              mimetype: file.mimetype,
              isZipExtracted: false,
              originalZipName: null,
            };
          }
        });

        await ProjectFile.bulkCreate(projectFilesData);
      }

      // Fetch the complete project with files
      const completeProject = await Project.findByPk(project.id, {
        include: [
          {
            model: ProjectFile,
            as: "files", // Make sure this matches your association alias
          },
        ],
      });

      return res.status(201).json({
        success: true,
        message: "Project created successfully",
        project: completeProject,
      });
    } catch (error) {
      console.error("Error creating project:", error);
      return res.status(500).json({ error: error.message });
    }
  }

  async updateProjectFirmware(projectId, newFirmwareVersion, userRole) {
    if (userRole !== "admin" && userRole !== "super_admin") {
      throw new Error("Unauthorized: Only admins can update project firmware");
    }

    const project = await Project.findByPk(projectId, {
      include: [
        {
          model: ProjectFile,
          as: "files",
        },
      ],
    });

    if (!project) {
      throw new Error("Project not found");
    }

    project.firmwareVersion = newFirmwareVersion;
    project.lastUpdated = new Date();
    await project.save();

    return project;
  }

  async getUserProjects(userId, userRole, options = {}) {
    const { page = 1, limit = 10 } = options;

    const whereCondition =
      userRole === "admin" || userRole === "super_admin" || userRole == "user"
        ? {} // No filter for admin/super_admin
        : { userId }; // Filter by user ID for regular users

    const { count, rows: projects } = await Project.findAndCountAll({
      where: whereCondition,
      include: [
        {
          model: ProjectFile,
          as: "files",
        },
      ],
      limit,
      offset: (page - 1) * limit,
      order: [["createdAt", "DESC"]],
    });

    return {
      projects,
      totalProjects: count,
      totalPages: Math.ceil(count / limit),
      currentPage: page,
    };
  }
  async deleteProject(projectId, userId, userRole) {
    const transaction = await sequelize.transaction();

    try {
      // Delete associated user project acquisitions first
      await UserProjectAcquisition.destroy({
        where: { projectId },
        transaction,
      });

      // Rest of the existing deletion logic remains the same
      const project = await Project.findByPk(projectId, {
        include: [{ model: ProjectFile, as: "files" }],
        transaction,
      });

      // Authorization and other checks...
      await ProjectFile.destroy({
        where: { projectId: project.id },
        transaction,
      });

      await project.destroy({ transaction });
      await transaction.commit();

      return project;
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  }

  async getCurrentUserVersion(userId) {
    const latestAcquisition = await UserProjectAcquisition.findOne({
      where: { userId },
      order: [["firmwareVersion", "DESC"]],
    });
    return latestAcquisition?.firmwareVersion || "1.0";
  }

  async getAcquiredProjects(userId, options) {
    // Updated to include device information and project files
    const { page = 1, limit = 10, deviceId } = options;
    const offset = (page - 1) * limit;

    // Build the where clause based on whether deviceId is provided
    const whereClause = {
      userId: userId,
      hasRemovalOccurred: false,
    };

    // If deviceId is provided, filter by that device
    if (deviceId) {
      whereClause.deviceId = deviceId;
    }

    const { count, rows } = await UserProjectAcquisition.findAndCountAll({
      where: whereClause,
      include: [
        {
          model: Project,
          as: "project",
          attributes: [
            "id",
            "name",
            "description",
            "imageUrl",
            "projectType",
            "youtubeLink",
            "version",
          ],
          include: [
            {
              model: ProjectFile,
              as: "files",
              attributes: [
                "id",
                "filename",
                "fileType",
                "fileSize",
                "filePath",
                "mimetype",
                "isZipExtracted",
                "originalZipName",
              ],
            },
          ],
        },
        {
          model: Device,
          as: "device",
          attributes: [
            "id",
            "deviceName",
            "deviceType",
            "firmwareVersion",
            "serialNumber",
          ],
        },
      ],
      limit: limit,
      offset: offset,
      order: [["createdAt", "DESC"]],
    });

    return {
      projects: rows,
      totalProjectsAcquired: count,
      currentPage: page,
      totalPages: Math.ceil(count / limit),
    };
  }

  async removeAcquiredProject(userId, projectId, deviceId) {
    // First check if the acquisition exists
    const acquisition = await UserProjectAcquisition.findOne({
      where: {
        userId: userId,
        projectId: projectId,
        deviceId: deviceId,
        hasRemovalOccurred: false,
      },
    });

    if (!acquisition) {
      throw new Error("Project acquisition not found");
    }

    // Get device information
    const device = await Device.findByPk(deviceId);

    // Mark the acquisition as removed
    acquisition.hasRemovalOccurred = true;
    await acquisition.save();

    // Count remaining projects for this device
    const remainingProjects = await UserProjectAcquisition.count({
      where: {
        deviceId: deviceId,
        hasRemovalOccurred: false,
      },
    });

    return {
      currentFirmwareVersion: device.firmwareVersion,
      remainingProjects: remainingProjects,
    };
  }

  async updateUserProjectFirmware(userId, projectId, newFirmwareVersion) {
    const acquisition = await UserProjectAcquisition.findOne({
      where: {
        userId,
        projectId,
      },
    });

    if (!acquisition) {
      throw new Error("Project acquisition not found");
    }

    acquisition.firmwareVersion = newFirmwareVersion;
    await acquisition.save();

    return acquisition;
  }

  incrementFirmwareVersion(version) {
    const versionNum = parseFloat(version);
    return (versionNum + 0.1).toFixed(1);
  }

  async acquireProject(userId, projectId, deviceId) {
    const transaction = await sequelize.transaction();

    try {
      const project = await Project.findByPk(projectId, { transaction });
      if (!project) {
        throw new Error("Project not found");
      }

      const device = await Device.findOne({
        where: {
          id: deviceId,
          userId: userId,
        },
        transaction,
      });

      if (!device) {
        throw new Error("Device not found or does not belong to this user");
      }

      const existingAcquisition = await UserProjectAcquisition.findOne({
        where: {
          userId: userId,
          projectId: projectId,
          deviceId: deviceId,
          hasRemovalOccurred: false,
        },
        transaction,
      });

      if (existingAcquisition) {
        throw new Error(
          "You have already acquired this project for this device"
        );
      }

      const deviceProjectCount = await UserProjectAcquisition.count({
        where: {
          deviceId: deviceId,
          hasRemovalOccurred: false,
        },
        transaction,
      });

      if (deviceProjectCount >= 5) {
        throw new Error(
          "This device already has the maximum of 5 projects. Please remove a project before adding a new one."
        );
      }

      const acquisition = await UserProjectAcquisition.create(
        {
          userId: userId,
          projectId: projectId,
          deviceId: deviceId,
          firmwareVersion: device.firmwareVersion,
          hasRemovalOccurred: false,
        },
        { transaction }
      );
     
      await transaction.commit();
       //!-------------------------------Update flag------------------------------
      await device.update(
        { isModified: true }, // new value
        { where: { id: deviceId } } // which row to update
      );
      //!-------------------------------------------------------------

      return {
        acquisition,
        firmwareVersion: device.firmwareVersion,
      };
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  }

  async removeAcquiredProject(userId, projectId, deviceId) {
    const transaction = await sequelize.transaction();

    try {
      const existingAcquisition = await UserProjectAcquisition.findOne({
        where: {
          userId,
          projectId,
          deviceId,
          hasRemovalOccurred: false,
        },
        transaction,
      });

      if (!existingAcquisition) {
        throw new Error("Project acquisition not found");
      }

      // Mark as removed
      existingAcquisition.hasRemovalOccurred = true;
      await existingAcquisition.save({ transaction });

      // Get device info
      const device = await Device.findByPk(deviceId, { transaction });

      // Count remaining projects
      const remainingProjects = await UserProjectAcquisition.count({
        where: {
          deviceId: deviceId,
          hasRemovalOccurred: false,
        },
        transaction,
      });

      //!-------------------------------Update flag------------------------------
      await device.update(
        { isModified: true }, // new value
        { where: { id: deviceId } } // which row to update
      );
      //!-------------------------------Update flag------------------------------
      await transaction.commit();

      return {
        success: true,
        currentFirmwareVersion: device.firmwareVersion,
        remainingProjects: remainingProjects,
      };
    } catch (error) {
      await transaction.rollback(); // rollback only here
      throw error;
    }
  }

  async getUserDevices(userId) {
    const devices = await Device.findAll({
      where: {
        userId: userId,
      },
      include: [
        {
          model: UserProjectAcquisition,
          as: "acquisitions",
          where: {
            hasRemovalOccurred: false,
          },
          required: false,
          include: [
            {
              model: Project,
              as: "project",
            },
          ],
        },
      ],
    });

    // For each device, add a count of projects
    const devicesWithCounts = devices.map((device) => {
      const deviceData = device.toJSON();
      deviceData.projectCount = device.acquisitions
        ? device.acquisitions.length
        : 0;
      return deviceData;
    });

    return devicesWithCounts;
  }
}

module.exports = new ProjectService();
