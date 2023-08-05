from flask import request
from flask_restful import Resource, marshal_with

from flask_autoapi.utils.response import APIResponse, resource_fields
from flask_autoapi.utils.message import BAD_REQUEST, OBJECT_SAVE_FAILED

class BaseEndpoint(Resource):

    Model = None
    Type = None
    decorators = [marshal_with(resource_fields)]

    @classmethod
    def add_decorators(cls, decorator_list):
        if not isinstance(decorator_list, (list, tuple)):
            raise Exception("格式错误")
        cls.decorators += decorator_list

    def get(self, id):
        """
        @api {GET} /{{project_name}}/{{ModelName.lower()}}/:id 获取{{Title}}详情
        @apiName Get{{ModelName}}
        @apiGroup {{Group}}

        @apiExample 返回值
        {
            "code": 0,
            "message":"",
            "data":{ {% for field in Fields %}
                {{ str_align('"'+field.name+'"') }}: \t {{get_example(standard_type(field.field_type), field.choices)}}  {% if field.verbose_name %} \t # {{field.verbose_name}} {% endif %}{% endfor %},
            }
        }

        """
        without_fields = request.args.get("without_fields")
        without_fields = without_fields.split(",") if without_fields else None
        r = self.Model.get_with_pk(id, without_fields)
        r = self.Model.to_json(r, without_fields) if r else None
        return APIResponse(data=r)
    
    def post(self):
        """
        @api {POST} /{{project_name}}/{{ModelName.lower()}} 创建{{Title}}
        @apiName Create{{ModelName}}
        @apiGroup {{Group}}

        @apiExample 参数
        {%- for field in Fields %}
        {{ str_align(standard_type(field.field_type))}} \t {{ str_align(field.name, 15) }}  # {% if field.null is sameas true %} 非必填项 {% else %} 必填项 {% endif %} {% if field.verbose_name %}, {{field.verbose_name}} {% endif %}{% endfor %}
        

        @apiExample 返回值
        {
            "code": 0,
            "message":"",
            "data":{ {% for field in Fields %}
                {{ str_align('"'+field.name+'"') }}: \t {{get_example(standard_type(field.field_type), field.choices)}}  {% if field.verbose_name %} \t # {{field.verbose_name}} {% endif %}{% endfor %},
            }
        }
        """
        params = request.get_json() if request.content_type == "application/json" else request.form.to_dict()
        params.update(request.files.to_dict())
        params = self.Model.format_params(**params)
        status = self.Model.verify_params(**params)
        if not status:
            return APIResponse(BAD_REQUEST)
        params = self.Model.upload_files(**params)
        if not self.Model.validate(**params):
            return APIResponse(BAD_REQUEST)
        r = self.Model.create(**params)
        r.save()
        r = self.Model.to_json(r) if r else None
        return APIResponse(data=r)
    
    def put(self, id):
        """
        @api {PUT} /{{project_name}}/{{ModelName.lower()}}/:id 更新{{Title}}
        @apiName Update{{ModelName}}
        @apiGroup {{Group}}

        @apiExample 参数
        {%- for field in Fields %}
        {{ str_align(standard_type(field.field_type))}} \t {{ str_align(field.name, 15) }}  # {% if field.null is sameas true %} 非必填项 {% else %} 必填项 {% endif %} {% if field.verbose_name %}, {{field.verbose_name}} {% endif %}{% endfor %}

        @apiExample 返回值
        {
            "code": 0,
            "message": "",
            "data":{ {% for field in Fields %}
                {{ str_align('"'+field.name+'"') }}: \t {{get_example(standard_type(field.field_type), field.choices)}}  {% if field.verbose_name %} \t # {{field.verbose_name}} {% endif %}{% endfor %},
            }
        }
        
        """
        params = request.get_json() if request.content_type == "application/json" else request.form.to_dict()
        params.update(request.files.to_dict())
        params = self.Model.format_params(**params)
        status = self.Model.verify_params(**params)
        if not status:
            return APIResponse(BAD_REQUEST)
        params = self.Model.upload_files(**params)
        if not self.Model.validate(**params):
            return APIResponse(BAD_REQUEST)
        r = self.Model.update_by_pk(id, **params)
        r = self.Model.to_json(r) if r else None
        return APIResponse(data=r)
    
    def delete(self, id):
        """
        @api {DELETE} /{{project_name}}/{{ModelName.lower()}}/:id 删除{{Title}}
        @apiName Delete{{ModelName}}
        @apiGroup {{Group}}

        @apiExample 返回值
        {
            "code": 0,
            "message": "",
            "data": None,
        }
        
        """
        self.Model.delete().where(self.Model._meta.primary_key == id).execute()
        return APIResponse()


class BaseListEndpoint(Resource):

    Model = None
    Type = "List"
    decorators = [marshal_with(resource_fields)]

    @classmethod
    def add_decorators(cls, decorator_list):
        if not isinstance(decorator_list, (list, tuple)):
            raise Exception("格式错误")
        cls.decorators += decorator_list

    def get(self):
        """
        @api {GET} /{{project_name}}/{{ModelName.lower()}}/list 获取{{Title}}列表
        @apiName Get{{ModelName}}List
        @apiGroup {{Group}}

        @apiExample 返回值
        {
            "code": 0,
            "message": null,
            "data": [
                { {% for field in Fields %}
                    {{ str_align('"'+field.name+'"') }}: \t {{get_example(standard_type(field.field_type), field.choices)}}  {% if field.verbose_name %} \t # {{field.verbose_name}} {% endif %}{% endfor %},
                }
            ],
        }
        """
        args = request.args.to_dict()
        args = self.Model.verify_list_args(**args)
        # if not args:
        #     return APIResponse(BAD_REQUEST)
        without_fields = request.args.get("without_fields")
        without_fields = without_fields.split(",") if without_fields else None
        fields = self.Model.get_fields()
        fields = [field for field in fields if field.name not in without_fields] \
                    if without_fields else fields
        result = self.Model.select(*fields)
        for key, value in args.items():
            result = result.where(getattr(self.Model, key) == value)
        result = [self.Model.to_json(r, without_fields) for r in result] if result else None
        return APIResponse(data=result)
        