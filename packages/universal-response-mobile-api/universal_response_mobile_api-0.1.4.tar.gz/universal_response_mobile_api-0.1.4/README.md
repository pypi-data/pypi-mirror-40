Library for django rest framework

**Install**

pip install universal-response-mobile-api

**Use**

import universal_response_mobile_api as u_mobile_api

**1. Decorator**
 
Add your Django project, for default behavior: 

file: `settings.py`
 
     import universal_response_mobile_api as u_mobile_api

    'DEFAULT_RENDERER_CLASSES': (
            'u_mobile_api.StructuredJsonRenderer',
        ),

or use as decorator for rest-api.


**2. Errors handler**

Add your Django project:

file: `settings.py`

    import universal_response_mobile_api as u_mobile_api

    REST_FRAMEWORK = {
        ...
        'EXCEPTION_HANDLER': 'u_mobile_api.custom_exception_handler',
        ...
    }


