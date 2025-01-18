
#!Ment for connect the assets to the app
from flask_assets import Environment, Bundle


from flask_assets import Environment, Bundle
def register_sass_folders(app):
    
    assets = Environment(app)
    
    #** admin assets
    try:
        admin_sass_bundle = Bundle(
                                './web/admin/static/sass/navstyle.scss',
                                filters='libsass', 
                                output='./web/admin/static/css/scss_convert.css', 
                                depends='./web/admin/static/sass/*.scss')
        
        assets.register('admin_sass_all', admin_sass_bundle)
        print('admin_sass_all registered')
    except Exception as e:
        print(e)
    
        
     #** Main_page assets
    #admin_sass_bundle = Bundle('static/sass/*.scss', filters='libsass', output='Main_page/static/css/Main_page_converted.css')
    #assests.register('Main_page_sass_all', admin_sass_bundle)
    
     #** login_page assets
    #admin_sass_bundle = Bundle('static/sass/*.scss', filters='libsass', output='login_page/static/css/login_page_converted.css')
    #assests.register('login_page_sass_all', admin_sass_bundle)
    
    
     
     #[Bundle('src/sass/admin/*.scss', filters='pyscss', output='dist/css/admin_styles.css')]
    
      #      - src/sass/admin/*.scss: the path to the scss files
            
      #      - filters='pyscss': the filter to use, in this case, we are using the pyscss filter
            
      #      - output='dist/css/admin_styles.css': the path to the output file, where the compiled css will be saved. In our case, it will be the css folder in the static directory.
            
            
      #       <link rel="stylesheet" href="{{ url_for('static', filename='css/admin_styles.css') }}" /> : I calll the converted file like this in the html file
    
    
    