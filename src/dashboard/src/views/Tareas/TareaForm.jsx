import React, { Component } from "react";
import { Col } from "react-bootstrap";

import { Card } from "components/Card/Card.jsx";
import { FormInputs } from "components/Form/Form.jsx";
import Button from "elements/CustomButton/CustomButton.jsx";

const fields = ["nombre", "recursos", "payoff", "hora"];

function safeParse(payload) {
  try {
    return JSON.parse(payload);
  } catch (e) {
    return null;
  }
}

class TareaForm extends Component {
  constructor(props) {
    super(props);

    this.validateTarea = this.validateTarea.bind(this);
    this.serialize = this.serialize.bind(this);
    this.saveTarea = this.saveTarea.bind(this);
    this.onSubmitTarea = this.onSubmitTarea.bind(this);
  }

  validateTarea(values) {
    for (const key in values) {
      if (values[key] === "") {
        return `Error: ${key} es requerido`;
      }
    }

    if (!Array.isArray(safeParse(values.recursos))) {
      return `Error: Los recursos deben estar ingresados como un array de recursos JSON. Ej. [1,2]`;
    }

    if (
      safeParse(values.recursos).some(recurso =>
        Number.isNaN(parseInt(recurso, 10))
      )
    ) {
      return `Error: Los recursos deben ser enteros`;
    }

    if (
      Number.isNaN(parseInt(values.hora, 10)) ||
      parseInt(values.hora, 10) < 0 ||
      parseInt(values.hora, 10) > 23
    ) {
      return `Error: La hora deben ser un entero entre 0 y 23`;
    }

    return null;
  }

  serialize(tarea) {
    return {
      ...tarea,
      hora: parseInt(tarea.hora, 10),
      payoff: parseInt(tarea.payoff, 10),
      recursos: safeParse(tarea.recursos).map(r => parseInt(r, 10))
    };
  }

  onSubmitTarea(e) {
    e.preventDefault();

    const tarea = Object.keys(e.target)
      .filter((a, i) => i < 4)
      .reduce(
        (obj, key, i) => ({
          ...obj,
          [fields[i]]: e.target[key].value
        }),
        {}
      );

    if (this.validateTarea(tarea) !== null) {
      alert(this.validateTarea(tarea));
    } else {
      this.saveTarea(this.serialize(tarea));
    }
  }

  saveTarea(tarea) {
    return this.props.addTarea(tarea);
  }

  render() {
    return (
      <Col md={12}>
        <Card
          title="Cargar Tarea"
          content={
            <form onSubmit={this.onSubmitTarea}>
              <FormInputs
                ncols={["col-md-5", "col-md-3", "col-md-2", "col-md-2"]}
                proprieties={[
                  {
                    label: "Nombre",
                    type: "text",
                    bsClass: "form-control",
                    placeholder: "Nombre..."
                  },
                  {
                    label: "Recursos",
                    type: "text",
                    bsClass: "form-control",
                    placeholder: "[1,2]"
                  },
                  {
                    label: "Payoff",
                    type: "number",
                    bsClass: "form-control",
                    placeholder: "0"
                  },
                  {
                    label: "Hora",
                    type: "number",
                    bsClass: "form-control",
                    placeholder: "0"
                  }
                ]}
              />

              <Button bsStyle="info" pullRight fill type="submit">
                Cargar Tarea
              </Button>
              <div className="clearfix" />
            </form>
          }
        />
      </Col>
    );
  }
}

export default TareaForm;
