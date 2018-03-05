import React, { Component } from "react";
import { Grid, Row, Col } from "react-bootstrap";
import Button from "elements/CustomButton/CustomButton.jsx";
import Satelite from "assets/img/satellite.svg";
import { StatsCard } from "components/StatsCard/StatsCard.jsx";

class Dashboard extends Component {
  createLegend(json) {
    var legend = [];
    for (var i = 0; i < json["names"].length; i++) {
      var type = "fa fa-circle text-" + json["types"][i];
      legend.push(<i className={type} key={i} />);
      legend.push(" ");
      legend.push(json["names"][i]);
    }
    return legend;
  }
  render() {
    const { satelites, tareas, resultados, ejecutarCampaña } = this.props;

    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-rocket text-warning" />}
                statsText="Satelites"
                statsValue={satelites.length}
                statsIcon={<i className="fa fa-refresh" />}
                statsIconText="En órbita ahora mismo"
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-wallet text-success" />}
                statsText="Payoff"
                statsValue={`$${resultados.reduce(
                  (payoffTotal, resultado) =>
                    payoffTotal +
                    resultado.reduce(
                      (payoffResultado, plan) =>
                        payoffResultado +
                        plan.results.reduce(
                          (payoffPlan, tarea) => tarea.resultado + payoffPlan,
                          0
                        ),
                      0
                    ),
                  0
                )}`}
                statsIcon={<i className="fa fa-calendar-o" />}
                statsIconText="Desde el comienzo de operaciones..."
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-graph1 text-danger" />}
                statsText="Fallos"
                statsValue={resultados.reduce(
                  (payoffTotal, resultado) =>
                    payoffTotal +
                    resultado.reduce(
                      (payoffResultado, plan) =>
                        payoffResultado +
                        plan.results.reduce(
                          (payoffPlan, tarea) =>
                            tarea.resultado === 0 ? 1 + payoffPlan : payoffPlan,
                          0
                        ),
                      0
                    ),
                  0
                )}
                statsIcon={<i className="fa fa-clock-o" />}
                statsIconText="Fallos satelitales"
              />
            </Col>
            <Col lg={3} sm={6}>
              <StatsCard
                bigIcon={<i className="pe-7s-note text-info" />}
                statsText="Tareas"
                statsValue={tareas.length}
                statsIcon={<i className="fa fa-refresh" />}
                statsIconText="Planificadas actualmente"
              />
            </Col>
          </Row>
          <Row>
            <Col lg={8} md={8} mdOffset={2} lgOffset={2} xs={12}>
              <Button
                style={{
                  width: "100%",
                  height: 150,
                  display: "flex",
                  justifyContent: "space-around",
                  alignItems: "center"
                }}
                bsStyle="info"
                pullRight
                fill
                onClick={ejecutarCampaña}
              >
                <span
                  style={{
                    fontSize: 36,
                    fontWeight: "bold"
                  }}
                >
                  EJECUTAR CAMPAÑA
                </span>
                <img src={Satelite} style={{ height: "50%" }} />
              </Button>
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default Dashboard;
