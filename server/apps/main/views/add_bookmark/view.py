from typing import cast
from urllib.parse import urlencode
from django.http import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from server.apps.main.forms.bookmarks import AddBookmarkWidgetForm
from server.apps.main.models.bookmark import LinkType
from server.apps.main.models.user import User
from server.apps.main.services.bookmark import create_bookmark
from render_block import render_block_to_string


class AddBookmarkView(View):
    template_name = "main/templates/add_bookmark/index.html"
    success_template_name = "main/templates/add_bookmark/success.html"

    def get(self, request, link: str | None = None):
        if not link:
            return HttpResponseRedirect(redirect_to=reverse("main:explore"))
        query_params = urlencode(request.GET)
        if query_params:
            link += "?" + query_params

        # title = extract_title_from_url(link)
        # link_type = guess_link_type(link)
        form = AddBookmarkWidgetForm(initial={"link": link})
        return render(
            request=request,
            template_name=self.template_name,
            context={"form": form},
        )

    def post(self, request: HttpRequest):
        user = cast(User, request.user)
        form = AddBookmarkWidgetForm(request.POST)
        context = {
            "form": form,
        }
        if not form.is_valid():
            return HttpResponse(
                render_block_to_string(
                    request=request,
                    template_name=self.template_name,
                    block_name="form",
                    context=context,
                )
            )

        form_data = form.cleaned_data
        collections = form_data["collections"]
        title = form_data["title"]
        link = form_data["link"]
        link_type = LinkType(form_data["link_type"])
        add_to_reading_list = form_data["add_to_reading_list"]

        create_bookmark(
            user=user,
            link=link,
            link_type=link_type,
            title=title,
            add_to_reading_list=add_to_reading_list,
            collections=collections,
        )

        return render(
            request=request,
            template_name=self.success_template_name,
            context={
                "link": link,
            },
        )
