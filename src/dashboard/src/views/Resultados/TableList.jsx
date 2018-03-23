import React, { Component } from "react";
import { Grid, Row, Col, Table } from "react-bootstrap";

import Card from "components/Card/Card.jsx";

const fields = ["nombre", "success_rate", "results"];
const fields_tarea = ["nombre", "resultado"];

class TableList extends Component {
  constructor(props) {
    super(props);

    this.renderResultado = this.renderResultado.bind(this);
    this.renderResultadoPlan = this.renderResultadoPlan.bind(this);
  }

  renderResultadoPlan(plan) {
    return (
      plan &&
      plan.map((tarea, key) => (
        <Table key={key} striped hover>
          <thead>
            <tr>
              {fields_tarea.map((field, key) => <th key={key}>{field}</th>)}
            </tr>
          </thead>
          <tbody>
            <tr key={key}>
              {fields_tarea.map((field, key) => (
                <td key={key}>{tarea[field]}</td>
              ))}
            </tr>
          </tbody>
        </Table>
      ))
    );
  }

  renderResultado(resultado, i) {
    return (
      <Card
        key={i}
        title={`Resultado ${i}`}
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
              {resultado.map((plan, skey) => {
                return (
                  <tr key={skey}>
                    {fields.map((prop, pkey) => {
                      const content =
                        prop === "results"
                          ? this.renderResultadoPlan(plan[prop])
                          : plan[prop];
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
    const { resultados } = this.props;

    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col md={12}>{resultados.map(this.renderResultado)}</Col>
          </Row>
        </Grid>
      </div>
    );
  }
}

export default TableList;
