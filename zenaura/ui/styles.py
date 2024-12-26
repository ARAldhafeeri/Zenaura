btn_one_class = """
inline-flex items-center justify-center 
whitespace-nowrap text-sm font-semibold 
transition-colors focus-visible:outline-none 
focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-primary 
disabled:pointer-events-none disabled:opacity-50 
shadow-md h-10 px-5 py-2 rounded-md 
m-2 bg-primary text-white hover:bg-primary-hover 
dark:bg-dark-primary dark:text-dark-text 
dark:hover:bg-dark-primary-hover
"""

btn_two_class = """
inline-flex items-center justify-center 
whitespace-nowrap text-sm font-medium 
transition-colors focus-visible:outline-none 
focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-secondary 
disabled:pointer-events-none disabled:opacity-50 
border border-gray-300 bg-gray-100 shadow-sm 
h-10 px-5 py-2 rounded-md 
m-2 text-gray-700 hover:bg-gray-200 
dark:bg-dark-gray dark:text-dark-text 
dark:border-dark-border dark:hover:bg-dark-gray-hover
"""

main_content = """
min-h-screen relative bg-light-background text-gray-800 
dark:bg-dark-background dark:text-dark-foreground 
p-6 mx-auto flex flex-col gap-4 
py-10 md:py-14 lg:py-20 max-w-screen-lg
"""

def with_theme_colors_text_no_hover(class_name):
    return f"""
    {class_name} 
    text-primary 
    dark:text-dark-text
    """

def with_theme_colors_text_no_hover(class_name):
  return f"{class_name} text-light-gray1 dark:text-dark-page1"


"""
// tailwind.config.js
module.exports = {
    theme: {
        extend: {
            colors: {
                primary: "#1a73e8",              // Professional blue
                "primary-hover": "#135bb3",     // Darker blue for hover
                "primary-foreground": "#ffffff", // White text
                secondary: "#6c757d",           // Neutral gray
                "secondary-hover": "#565e64",   // Darker neutral gray
                "light-gray1": "#f1f3f5",       // Light background
                "light-white": "#ffffff",       // White
                "light-green": "#34d399",       // Accent green
                "dark-primary": "#1e293b",      // Dark blue
                "dark-primary-hover": "#16233b",// Hover dark blue
                "dark-background": "#121212",   // Dark mode background
                "dark-text": "#e0e0e0",         // Light text for dark mode
                "dark-accent": "#2563eb",       // Dark mode accent
                "dark-border": "#333333",       // Border color in dark mode
                "dark-gray": "#1f2937",         // Dark mode gray
                "dark-gray-hover": "#374151",   // Hover dark mode gray
            },
        },
    },
};
"""