#设置导入功能
from django.template.context_processors import csrf

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


#excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, request, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html'))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)