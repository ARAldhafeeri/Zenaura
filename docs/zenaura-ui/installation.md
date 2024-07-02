# Installing zenaura 

prerequisits:
    - Python 3.12 or above.
    - node
    - zenaura v0.12.0

## Step 1 : install zenaura
```bash
pip zenaura==0.12.0
```
## step 2 : Configure tailwind css for use in zenaura 
#### 1. Install tailwind and init configuration 

```
npm install -D tailwindcss
npx tailwindcss init
```

#### adding paths 

Add the paths to all of your template files in your tailwind.config.js file, as follow:
```
module.exports = {
  content: [
    './public/index.html', "./public/**/*.py"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

#### Configure main.css

add the following directives to your main css file.

```
@tailwind base;
@tailwind components;
@tailwind utilities;
```

#### add components

create components folder inside your puplic folder, add compomonents files into config.json e.g. components/common.py

```
{
    / ... same
    "fetch": [
      {
        "files": [
          / ... same 
          
          "./public/components/common.py",


        ]
      }
    ],
    / ... same
    }
  }
```

#### run zenaura with tailwind css 

 open terminal and use zenaura cli to run build and run zenaura application.

```
zenaura build
zenaura run
```

add output.css to your build.py stylesheets

```
from zenaura.server import ZenauraServer
from public.main import my_app_layout

ZenauraServer.hydrate_app_layout(my_app_layout, scripts=[
        # same
        '<link rel="stylesheet" href="public/gigavolt.min.css">',
        # same
])
```
open terminal and run tailwind css watch to create output.css 
```
npx tailwindcss -i ./src/input.css -o ./src/output.css --watch

```

Done ! Now when you start coding and add class names to your zenaura components tailwind css will add those styles to output.css