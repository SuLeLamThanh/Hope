from appbook import admin, db, app, dao
from appbook.models import Category, Product, UserRole, Tag
from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, request
import utils
from datetime import datetime
from wtforms import TextAreaField
from wtforms.widgets import TextArea

#
# class AuthenticatedModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)
#
#
# class ProductView(AuthenticatedModelView):
#     column_display_pk = True
#     can_view_details = True
#     can_export = True
#     column_searchable_list = ['name', 'description']
#     column_filters = ['name', 'price']
#     column_exclude_list = ['image', 'active', 'created_date']
#     column_labels = {
#         'name': 'Tên sản phẩm',
#         'description': 'Mô tả',
#         'price': 'Giá',
#         'image': 'Ảnh',
#         'category': 'Danh mục'
#     }
#     column_sortable_list = ['id', 'name', 'price']
#
#
# class LogoutView(BaseView):
#     @expose('/')
#     def index(self):
#         logout_user()
#         return redirect('/admin')
#
#     def is_accessible(self):
#         return current_user.is_authenticated
#
#
# class MyAdminIndex(AdminIndexView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/index.html', stats=utils.category_stats())
#
#
# admin = Admin(app=app, name='Quản trị bán hàng', template_mode='bootstrap4', index_view=MyAdminIndex())
# admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
# admin.add_view(ProductView(Product, db.session, name='Sản phẩm'))
# admin.add_view(LogoutView(name='Đăng xuất'))


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductView(AuthenticatedModelView):
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'author']
    column_filters = ['name', 'author']
    column_exclude_list = ['image', 'active', 'created_date']
    column_labels = {
        'name': 'Tên sp',
        'author': 'Tên tác giả',
        'description':'Mô tả',
        'price': 'Giá',
        'quantity': 'Số lượng',
        'image':'Ảnh đại diện',
         'category': 'Danh mục'
    }
    column_sortable_list = ['id', 'name', 'author', 'price', 'quantity']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
    page_size = 5


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_product_by_cate()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='Quản trị bán hàng',
              template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(AuthenticatedModelView(Category, db.session, name='Thể Loại'))
admin.add_view(ProductView(Product, db.session, name='Sách'))
admin.add_view(AuthenticatedModelView(Tag, db.session, name='Tag'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
