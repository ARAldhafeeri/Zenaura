class Router {
    constructor() {
      this.routes = {};
      this.defaultRoute = "";
      window.addEventListener("popstate", this.onpopstate);
    }
  
    // register a new route
    addRoute = (route, template) => {
      this.routes[route] = template;
    };
  
    // resolve current route from url
    resolveRoute = () => {
      const currentRoute = window.location.pathname;
      this.goTo(currentRoute === "/" ? this.defaultRoute : currentRoute);
    };
  
    // go to a specific route.
    goTo = (route) => {
      const content = this.routes[route];
  
      if (!content) {
        // Fallback to default route if route not found.
        this.goTo(this.defaultRoute);
        return;
      }
      this.renderContent(content, route);
      window.history.pushState({ content, title: route }, route, route);
    };
  
    // set default route.
    setDefault = (route) => {
      this.defaultRoute = route;
    };
  
    // handle history change event
    onpopstate = (e) => {
      if (e.state) {
        this.renderContent(e.state.content, e.state.title);
      }
    };
  
    // render view in content placeholder
    renderContent = (content, title) => {
      let templateDiv = document.getElementById("content");
      templateDiv.innerHTML = content;
      document.title = title;
    };
  }

  // example 

  
// instance of Router
const router = new Router();

// register routes with Router
const configureRoutes = () => {
  router.addRoute("/about", "<div>About me</div>");
  router.addRoute("/home", "<div>Custom client router</div>");
  router.addRoute("/contact", "<div>clientrouter@xyz.com</div>");
  router.setDefault("/home");
};

configureRoutes();
// Tell router to resolve current route on app load. Will route to default route in case of invalid one.
router.resolveRoute();

// attach routes to buttons
const element = (id) => document.getElementById(id);
const registerClickHandler = (id, route) =>
  element(id).addEventListener("click", () => router.goTo(route));

const addEventListeners = () => {
  registerClickHandler("about", "/about");
  registerClickHandler("home", "/home");
  registerClickHandler("contact", "/contact");
};

window.addEventListener("load", addEventListeners);