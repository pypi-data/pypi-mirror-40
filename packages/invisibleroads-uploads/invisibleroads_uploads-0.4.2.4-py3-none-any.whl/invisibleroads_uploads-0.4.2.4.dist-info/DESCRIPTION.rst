InvisibleRoads Uploads
======================
Add basic file upload functionality to your Pyramid app.

Use
---
Prepare environment. ::

    export VIRTUAL_ENV=~/.virtualenvs/crosscompute
    virtualenv ${VIRTUAL_ENV}
    source ${VIRTUAL_ENV}/bin/activate

    export NODE_PATH=${VIRTUAL_ENV}/lib/node_modules
    npm install -g browserify uglify-js

Install package. ::

    cd ~/Projects/invisibleroads-uploads
    python setup.py develop
    bash refresh.sh

Add settings. ::

    upload.id.length = 32

Configure views. ::

    config.include('invisibleroads_uploads')

Call template macro. ::

    {% from 'invisibleroads_uploads:templates/parts.jinja2' import upload_button %}
    {{ upload_button(request, id='xyz-upload', text='Browse for xyz', class='xyz') }}

Add callback and activate button. ::

    $('#xyz-upload').on('uploaded.ir', function(e, d) {
      console.log(d.upload_id);
    }).enable();

0.4
---
- Define Upload.save, Upload.save_from, Upload.load
- Replace get_upload_from with Upload.get_from

0.3
---
- Handle HTTP status code 413 Payload Too Large

0.2
---
- Ignore multiple clicks on upload button until dialog closes
- Replace uploaded.ir.upload with uploaded.ir

0.1
---
- Add basic upload functionality
- Ignore multiple clicks on upload button for a few seconds

