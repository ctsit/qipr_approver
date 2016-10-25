from django.shortcuts import redirect

from approver.workflows import project_crud
from approver.decorators import login_required
import approver.utils as utils
from django.core.urlresolvers import reverse

@login_required
def similar_projects(request, project_id=None,from_page=None):
    
    project = project_crud.get_project_or_none(project_id)

    if project is None:
        utils.dashboard_redirect_and_toast(request, 'Invalid request'.format(project_id))
    elif request.method == 'GET':
        project_scores = project_crud.get_similar_projects(project)

        if (len(project_scores) == 0) :
            utils.set_toast(request.session, 'No relevant projects were found!')
            if(from_page == "dashboard") :
                return redirect(reverse("approver:dashboard"))
            else :
                return redirect(reverse("approver:approve") + str(project.id) + '/')

        context = {
                    'content': 'approver/similar_projects.html',
                    'project_scores': project_scores,
                    'project_id' : project_id,
                }        
        return utils.layout_render(request, context)

    elif request.method == 'POST':
        return redirect(reverse("approver:approve") + str(project.id) + '/')