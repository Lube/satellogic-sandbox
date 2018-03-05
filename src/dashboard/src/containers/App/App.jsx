import React, { Component } from "react";
import { Route, Switch, Redirect } from "react-router-dom";

import {
  getTareas,
  getSatelites,
  getAsignaciones,
  getResultados,
  addTarea,
  ejecutarCampaña
} from "api/api";

import Sidebar from "components/Sidebar/Sidebar";

import appRoutes from "routes/app.jsx";

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      satelites: [],
      tareas: [],
      asignaciones: [],
      resultados: []
    };

    this.updateEntities = this.updateEntities.bind(this);
  }

  async updateEntities() {
    const [satelites, tareas, asignaciones, resultados] = await Promise.all([
      getSatelites(),
      getTareas(),
      getAsignaciones(),
      getResultados()
    ]);

    this.setState({
      satelites,
      tareas,
      asignaciones,
      resultados
    });
  }

  componentDidMount() {
    setInterval(this.updateEntities, 2000);
  }

  componentDidUpdate(e) {
    if (
      window.innerWidth < 993 &&
      e.history.location.pathname !== e.location.pathname &&
      document.documentElement.className.indexOf("nav-open") !== -1
    ) {
      document.documentElement.classList.toggle("nav-open");
    }
  }

  render() {
    return (
      <div className="wrapper">
        <Sidebar {...this.props} />
        <div id="main-panel" className="main-panel">
          <Switch>
            {appRoutes.map((prop, key) => {
              if (prop.name === "Notifications")
                return (
                  <Route
                    path={prop.path}
                    key={key}
                    render={routeProps => (
                      <prop.component
                        {...routeProps}
                        handleClick={this.handleNotificationClick}
                      />
                    )}
                  />
                );
              if (prop.redirect)
                return <Redirect from={prop.path} to={prop.to} key={key} />;
              return (
                <Route
                  path={prop.path}
                  render={() => (
                    <prop.component
                      {...this.state}
                      addTarea={addTarea}
                      ejecutarCampaña={ejecutarCampaña}
                    />
                  )}
                  key={key}
                />
              );
            })}
          </Switch>
        </div>
      </div>
    );
  }
}

export default App;
