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
            "data":{ {% for field in AllFields %}
                {{ str_align('"'+field.name+'"') }}: \t {% if is_mtom(field) is sameas false %} {{get_example(standard_type(field.field_type), field.choices)}} {% if field.verbose_name %} \t # {{field.verbose_name}} {% endif %} {% else %} 
                [
                    { {% for f in mtom_fields(field) %} 
                        {{ str_align('"'+f.name+'"') }}: \t {{get_example(standard_type(f.field_type), f.choices)}}{% endfor %}
                    }
                ]
                {% endif %} {% endfor %}
            }
        }

        """
        without_fields = request.args.get("without_fields")
        without_fields = without_fields.split(",") if without_fields else None
        r = self.Model.get_with_pk(id, without_fields)
        r = self.Model.to_json(r, without_fields) if r else None
        r = self.Model.out_handlers(**r)
        r = self.Model.diy_after_get(**r)
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
            "data":{ {% for field in AllFields %}
                {{ str_align('"'+field.name+'"') }}: \t {% if is_mtom(field) is sameas false %} {{get_example(standard_type(field.field_type), field.choices)}} {% if field.verbose_name %} \t # {{field.verbose_name}} {% endif %} {% else %} 
                [
                    { {% for f in mtom_fields(field) %} 
                        {{ str_align('"'+f.name+'"') }}: \t {{get_example(standard_type(f.field_type), f.choices)}}{% endfor %}
                    }
                ]
                {% endif %} {% endfor %}
            }
        }
        """
        params = request.get_json() if request.content_type == "application/json" else request.form.to_dict()
        params.update(request.files.to_dict())
        params = self.Model.in_handlers(**params)
        params = self.Model.format_params(**params)
        status = self.Model.verify_params(**params)
        if not status:
            return APIResponse(BAD_REQUEST)
        params = self.Model.upload_files(**params)
        if not self.Model.validate(**params):
            return APIResponse(BAD_REQUEST)
        self.Model.diy_before_save(**params)
        r = self.Model.create(**params)
        r.save()
        r.mtom(**params)
        r = self.Model.to_json(r) if r else None
        r = self.Model.out_handlers(**r)
        r = self.Model.diy_after_get(**r)
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
            "data":{ {% for field in AllFields %}
                {{ str_align('"'+field.name+'"') }}: \t {% if is_mtom(field) is sameas false %} {{get_example(standard_type(field.field_type), field.choices)}} {% if field.verbose_name %} \t # {{field.verbose_name}} {% endif %} {% else %} 
                [
                    { {% for f in mtom_fields(field) %} 
                        {{ str_align('"'+f.name+'"') }}: \t {{get_example(standard_type(f.field_type), f.choices)}}{% endfor %}
                    }
                ]
                {% endif %} {% endfor %}
            }
        }
        
        """
        params = request.get_json() if request.content_type == "application/json" else request.form.to_dict()
        params.update(request.files.to_dict())
        params = self.Model.in_handlers(**params)
        params = self.Model.format_params(**params)
        status = self.Model.verify_params(**params)
        if not status:
            return APIResponse(BAD_REQUEST)
        params = self.Model.upload_files(**params)
        if not self.Model.validate(**params):
            return APIResponse(BAD_REQUEST)
        self.Model.diy_before_save(**params)
        r = self.Model.update_by_pk(id, **params)
        r.mtom(**params)
        r = self.Model.to_json(r) if r else None
        r = self.Model.out_handlers(**r)
        r = self.Model.diy_after_get(**r)
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
        @api {GET} /{{project_name}}/{{ModelName.lower()}}/list?page=2&num=10&order=0 获取{{Title}}列表
        @apiName Get{{ModelName}}List
        @apiGroup {{Group}}

        @apiExample 参数
        int    page    # 页码。非必填，默认1。
        int    num     # 每页数量。非必填，默认10。
        int    order   # 排序方法。非必填，默认0。0表示按时间倒序，1表示按时间顺序。

        @apiExample 返回值
        {
            "code": 0,
            "message": null,
            "data": [
                { {% for field in AllFields %}
                    {{ str_align('"'+field.name+'"') }}: \t {% if is_mtom(field) is sameas false %} {{get_example(standard_type(field.field_type), field.choices)}} {% if field.verbose_name %} \t # {{field.verbose_name}} {% endif %} {% else %} 
                    [
                        { {% for f in mtom_fields(field) %} 
                            {{ str_align('"'+f.name+'"') }}: \t {{get_example(standard_type(f.field_type), f.choices)}}{% endfor %}
                        }
                    ]
                    {% endif %} {% endfor %}
                }
            ],
        }
        """
        args = request.args.to_dict()
        args = self.Model.verify_list_args(**args)
        try:
            page  = int(args.get("page", 1))
            num   = int(args.get("num", 10))
            order = int(args.get("order", 0))
        except:
            return APIResponse(BAD_REQUEST)
        if not order in (0, 1):
            return APIResponse(BAD_REQUEST)
        without_fields = request.args.get("without_fields")
        without_fields = without_fields.split(",") if without_fields else None
        fields = self.Model.get_fields()
        fields = [field for field in fields if field.name not in without_fields] \
                    if without_fields else fields
        result = self.Model.select(*fields)
        for key, value in args.items():
            result = result.where(getattr(self.Model, key) == value)
        result = result.order_by(self.Model.create_time.desc()) if order == 0 else result.order_by(self.Model.create_time.asc())
        result = result.offset((page-1)*num).limit(num)
        result = [self.Model.to_json(r, without_fields) for r in result] if result else None
        result = [self.Model.out_handlers(**r) for r in result]
        result = [self.Model.diy_after_get(**r) for r in result]
        return APIResponse(data=result)
        