from rest_framework import mixins, viewsets


class BaseListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''Base list view for brief and extend views'''
    queryset = None
    queryset_brief = None
    serializer_class = None
    serializer_class_brief = None

    def get_queryset(self):
        if self.request.GET.get('brief') and self.action == 'list':
            return self.queryset_brief
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.GET.get('brief') and self.action == 'list':
            return self.serializer_class_brief
        return super().get_serializer_class()


class BaseGetView(BaseListView, mixins.RetrieveModelMixin):
    '''Base get view for list and retrieve views'''
    queryset = None
    queryset_brief = None
    serializer_class = None
    serializer_class_brief = None
