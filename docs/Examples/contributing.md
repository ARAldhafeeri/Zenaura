# Contributing to zenaura examples:
The following guide shows steps to contribute your example so it can be featured on zenaura documentation page.

1. Create the example Repo on GitHub. 
2. Test the example make sure it's working.
3. Fork zenaura.
4. Create pull request where you add the example into the proper example section:
    + docs/examples/basic/my_example.md
    + docs/examples/intermediate/my_example.md
    + docs/examples/advanced/my_example.md
5. Make sure you correctly set the difficulty of the example, basic example should touch on zenaura basics, intermediate example should touch on zenaura intermediate and advanced example should touch on zenaura advanced.
6. Create your example markdown with the following format, copy template.md :
    + Author: authorName
    + Title: title of the example
    + Description: Brief description of the example.
    + Example GitHub URL.
7. add your example to mkdocs.yml
```
 - Basic Examples:
      - A counter app: examples/basic/counter.md
      - My Example Name: examples/basic/my_example.md # here
    - Beyond The Basics Examples:
      - Cory Game of Life: examples/intermediate/game_of_life.md
    - Advanced Examples:
      - Admin Portal: examples/advanced/admin_portal.md
```
8. create pull request.

