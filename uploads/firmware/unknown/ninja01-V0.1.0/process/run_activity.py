

from activity1.pactivity import run_activity as run_activity1
from activity2.pactivity import run_activity as run_activity2
from activity3.pactivity import run_activity as run_activity3
from activity4.pactivity import run_activity as run_activity4
from activity5.pactivity import run_activity as run_activity5

from process.route_activity import route_activity



def run(project_name):
    activity= route_activity(project_name)
    if activity=="activity1":
        run_activity1(activity)
    elif activity=="activity2":
        run_activity2(activity)
    elif activity=="activity3":
        run_activity3(activity)
    elif activity=="activity4":
        run_activity4(activity)
    elif activity=="activity5":
        run_activity5(activity)
