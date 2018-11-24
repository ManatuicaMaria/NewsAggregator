from django.shortcuts import render
from django.shortcuts import redirect

URL = "https://google.com"
DUMMY_DESCRITION="Lorem ipsum dolor sit amet, consectetur adipiscing elit. In luctus lobortis luctus. Duis eget lacus ultrices, aliquam arcu id, interdum quam. Praesent sollicitudin cursus blandit. Vestibulum ut libero semper, iaculis arcu et, vehicula felis. Pellentesque interdum ornare felis. Praesent at felis lacus. Etiam ac dapibus felis, sed faucibus lectus. Vestibulum ullamcorper eros eu diam ornare, auctor faucibus erat laoreet. Phasellus lobortis dolor at scelerisque pretium. Nulla facilisi. Nam et commodo dui. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nullam molestie sapien sed est auctor sollicitudin."
FAKE = "FAKE"
REAL = "REAL"
class Article:

    def __init__(self, title, description, url, date, fake, real_degree):
        self.title = title
        self.description = description
        self.url = url
        self.date = date
        self.fake = fake == FAKE
        self.real_degree = real_degree


def search(request):
    if request.POST:
        # TODO: Hook up query with elastic interface
        # TODO: paginare sau maxim 30 entries
        print(request.POST['query'])
        # articles = {"title": "title"}
        articles = [Article("title" + str(i), DUMMY_DESCRITION, URL, "24-11-2018", FAKE, 80) if i == 0 \
            else Article("title" + str(i), DUMMY_DESCRITION, URL, "24-11-2018", REAL, 80) for i in range(5)]
        return render(request, 'list.html', {'articles': articles})
    else:
        return render(request, 'list.html')