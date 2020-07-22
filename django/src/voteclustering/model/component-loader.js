export default new function () {
    this.registerGlobal = (componentLoader) => {
        componentLoader.keys().forEach(fileName => {
            const component = componentLoader(fileName);
            Vue.component(fileName.split('/').pop().replace(/\.\w+$/, ''), component.default || component)
        })
    }

    this.readRoutes = (componentLoader, pathPrefix) => {
        pathPrefix = pathPrefix || "";
        var routes = [];
        const indexChecker = /\/index$/;
        componentLoader.keys().forEach(fileName => {
            const component = componentLoader(fileName);

            var path = fileName.replace(/\.\w+$/, '').replace(/^\.+/, '');
            while (true) {

                var subRoutes = component.routes || [""];
                for (var subRoute of subRoutes) {
                    const appendedPath = pathPrefix + path + subRoute
                    routes.push({
                        path: appendedPath.length > 0 ? appendedPath : "/",
                        component: component.default || component
                    });
                }

                if (indexChecker.test(path)) {
                    path = path.replace(indexChecker, "");
                } else {
                    break;
                }
            }
        });

        routes.push({
            path: '*',
            component: {
                template: "<div>404 Not Found.</div>"
            }
        });

        return routes;
    }
}
