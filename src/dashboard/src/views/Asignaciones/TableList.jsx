import React, { Component } from "react";
import { Grid, Row, Col, Table } from "react-bootstrap";

import Card from "components/Card/Card.jsx";

const fields = ["nombre", "success_rate", "plan"];
const fields_tarea = ["recursos", "payoff", "hora", "nombre"];

class TableList extends Component {
  constructor(props) {
    super(props);

    this.renderAsignacion = this.renderAsignacion.bind(this);
    this.renderPlan = this.renderPlan.bind(this);
  }

  renderPlan(tareas, key) {
    return tareas.map(tarea => (
      <Table striped hover>
        <thead>
          <tr>
            {fields_tarea.map((field, key) => <th key={key}>{field}</th>)}
          </tr>
        </thead>
        <tbody>
          <tr key={key}>
            {fields_tarea.map((field, key) => (
              <td key={key}>{JSON.stringify(tarea[field])}</td>
            ))}
          </tr>
        </tbody>
      </Table>
    ));
  }

  renderAsignacion(asignacion, i) {
    return (
      <Card
        title={`Asignación ${i}`}
        ctTableFullWidth
        ctTableResponsive
        content={
          <Table striped hover>
            <thead>
              <tr>
                {fields.map((prop, key) => {
                  return <th key={key}>{prop}</th>;
                })}
              </tr>
            </thead>
            <tbody>
              {asignacion.map((satelite, skey) => {
                return (
                  <tr key={skey}>
                    {fields.map((prop, pkey) => {
                      const content =
                        prop === "plan"
                          ? this.renderPlan(satelite[prop])
                          : satelite[prop];
                      return <td key={pkey}>{content}</td>;
                    })}
                  </tr>
                );
              })}
            </tbody>
          </Table>
        }
      />
    );
  }

  render() {
    const { asignaciones } = this.props;

    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col md={12}>{asignaciones.map(this.renderAsignacion)}</Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default TableList;
