import React, { Component } from "react";
import { Grid, Row, Col, Table } from "react-bootstrap";

import Card from "components/Card/Card.jsx";
import TareaForm from "./TareaForm.jsx";

const fields = ["nombre", "recursos", "payoff", "hora"];

class TableList extends Component {
  render() {
    const { tareas, addTarea } = this.props;

    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col md={12}>
              <Card
                title="Tareas"
                category="Tareas disponibles actualmente"
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
                      {tareas.map((tarea, key) => {
                        return (
                          <tr key={key}>
                            {fields.map((prop, key) => {
                              return (
                                <td key={key}>{JSON.stringify(tarea[prop])}</td>
                              );
                            })}
                          </tr>
                        );
                      })}
                    </tbody>
                  </Table>
                }
              />
            </Col>
          </Row>
          <TareaForm addTarea={addTarea} />
        </Grid>
      </div>
    );
  }
}

export default TableList;
