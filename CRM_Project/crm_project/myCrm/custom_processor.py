
def load_css(request):

    css_mapping = {
        "": 'css/register.css',
        'signUp': 'css/register.css',
        'home': 'css/home.css',
        'add_record': 'css/add_record.css',
        'update': 'css/add_record.css'

    }

    current_page = request.path_info.lstrip('/').split('/')[0]
    css_file_path = css_mapping.get(current_page)
    
    return {'load_css': css_file_path}