btn_one_class = """
inline-flex items-center justify-center 
whitespace-nowrap text-sm font-medium 
transition-colors focus-visible:outline-none 
focus-visible:ring-1 focus-visible:ring-ring 
disabled:pointer-events-none disabled:opacity-50 
text-primary-foreground shadow 
h-9 px-4 py-2 rounded-[6px]
m-1 bg-light-gray1 text-light-white
hover:bg-light-green
dark:text-dark-page1
dark:bg-dark-black
dark:hover:bg-dark-gray2
"""

btn_two_class ="""
inline-flex items-center justify-center whitespace-nowrap 
text-sm font-medium transition-colors focus-visible:outline-none 
focus-visible:ring-1 focus-visible:ring-ring 
disabled:pointer-events-none disabled:opacity-50 
border border-input bg-background shadow-sm
h-9 px-4 py-2 rounded-[6px]
m-1 bg-light-white text-light-gray1
hover:text-light-green
dark:text-dark-black
dark:hover:bg-dark-gray2
dark:bg-dark-gray1
"""

main_content = "min-h-screen  p-4 relative bg-light-white dark:bg-dark-gray1 mx-auto flex flex-col gap-2 py-8 md:py-12 md:pb-8 lg:py-24 lg:pb-20 "

def with_theme_colors(class_name):
  return f"{class_name} text-light-gray1 hover:text-light-green dark:text-dark-page1 dark:hover:text-dark-gray2"

def with_theme_colors_text_no_hover(class_name):
  return f"{class_name} text-light-gray1 dark:text-dark-page1"