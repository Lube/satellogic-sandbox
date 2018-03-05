import React, { Component } from "react";
import { Grid, Row, Col, Table } from "react-bootstrap";

import Card from "components/Card/Card.jsx";

const fields = ["nombre", "success_rate", "status"];

class TableList extends Component {
  render() {
    const { satelites } = this.props;

    return (
      <div className="content">
        <Grid fluid>
          <Row>
            <Col md={12}>
              <Card
                title="Satelites"
                category="Satelites online"
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
                      {satelites.map((tarea, key) => {
                        return (
                          <tr key={key}>
                            {fields.map((prop, key) => {
                              return <td key={key}>{tarea[prop]}</td>;
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
        </Grid>
      </div>
    );
  }
}

export default TableList;
