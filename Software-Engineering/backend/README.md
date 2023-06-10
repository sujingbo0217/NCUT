# Usage

```shell
cd backend
conda create -n ncut python=3.9.16
pip install pip-tools
pip-compile
pip install -r requirements.txt

mkdir media
mkdir mnist/migrations

chmod +x migrate.sh
./migrate.sh
```
# ⚠️
**Modify** `.../python3.9/site-packages/drf_yasg/inspectors/view.py` from line 165, for not throwing exception for incoming variables of type `openapi.IN_FORM`.  

- Before:
   ```python
   if any(param.in_ == openapi.IN_FORM for param in manual_parameters):  # pragma: no cover
       has_body_parameter = any(param.in_ == openapi.IN_BODY for param in parameters)
       if has_body_parameter or not any(is_form_media_type(encoding) for encoding in self.get_consumes()):
           raise SwaggerGenerationError("cannot add form parameters when the request has a request body; "
                                             "did you forget to set an appropriate parser class on the view?")
       if self.method not in self.body_methods:
           raise SwaggerGenerationError("form parameters can only be applied to "
                                             "(" + ','.join(self.body_methods) + ") HTTP methods")
   ```
    
- After
   ```python
   if any(param.in_ == openapi.IN_FORM for param in manual_parameters):  # pragma: no cover
       has_body_parameter = any(param.in_ == openapi.IN_BODY for param in parameters)
       # if has_body_parameter or not any(is_form_media_type(encoding) for encoding in self.get_consumes()):
       #     raise SwaggerGenerationError("cannot add form parameters when the request has a request body; "
       #                                       "did you forget to set an appropriate parser class on the view?")
       if self.method not in self.body_methods:
           raise SwaggerGenerationError("form parameters can only be applied to "
                                             "(" + ','.join(self.body_methods) + ") HTTP methods")
   ```
