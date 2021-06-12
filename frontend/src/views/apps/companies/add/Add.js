import React from "react"
import {
  Card,
  CardBody,
  Row,
  Col,
  Nav,
  NavItem,
  NavLink,
  TabContent,
  TabPane
} from "reactstrap"
import classnames from "classnames"
import { Briefcase, Columns, Settings } from "react-feather"
import Company from "./Company"
import Hierarchy from "./Hierarchy"
import "../../../../assets/scss/pages/users.scss"
import Breadcrumbs from "../../../../components/@vuexy/breadCrumbs/BreadCrumb"
import Machine from "./Machine"
import axios from "axios"
import { GET_COMPANIES_ENDPOINT } from "../../../../config"

class AddCompany extends React.Component {
  state = {
    activeTab: "1",
    company: 0,
    companyName: "Seleccione una opción",
    companies: [{ id: 0, name: "Seleccione una opción" }],
  }

  toggle = tab => {
    this.setState({
      activeTab: tab
    })
  }

  async componentDidMount() {
    try {
      const res = await axios.get(GET_COMPANIES_ENDPOINT)
      this.setState({ companies: [{ id: 0, name: "Seleccione una opción" }, ...res.data] })
    } catch (e) {
      console.log(e);
      const alertData = {
        title: "Error de Conexión",
        success: false,
        show: true,
        alertText: "Error al Conectar al Servidor"
      }
      this.props.displayAlert(alertData)
    }
  }

  render() {
    return (
      <React.Fragment>
        <Breadcrumbs
          breadCrumbTitle="Agregar"
          breadCrumbParent="Empresas"
          breadCrumbActive="Agregar"
        />
        <Row>
          <Col sm="12">
            <Card>
              <CardBody className="pt-2">
                <Nav tabs>
                  <NavItem>
                    <NavLink
                      className={classnames({
                        active: this.state.activeTab === "1"
                      })}
                      onClick={() => { this.toggle("1") }}
                    >
                      <Briefcase size={16} />
                      <span className="align-middle ml-50">Empresa</span>
                    </NavLink>
                  </NavItem>
                  <NavItem>
                    <NavLink
                      className={classnames({
                        active: this.state.activeTab === "2"
                      })}
                      onClick={() => { this.toggle("2") }}
                    >
                      <Columns size={16} />
                      <span className="align-middle ml-50">Jerarquía</span>
                    </NavLink>
                  </NavItem>
                  <NavItem>
                    <NavLink
                      className={classnames({
                        active: this.state.activeTab === "3"
                      })}
                      onClick={() => { this.toggle("3") }}
                    >
                      <Settings size={16} />
                      <span className="align-middle ml-50">Máquina</span>
                    </NavLink>
                  </NavItem>
                </Nav>
                <TabContent activeTab={this.state.activeTab}>
                  <TabPane tabId="1">
                    <Company />
                  </TabPane>
                  <TabPane tabId="2">
                    <Hierarchy companies={this.state.companies} />
                  </TabPane>
                  <TabPane tabId="3">
                    <Machine companies={this.state.companies} />
                  </TabPane>
                </TabContent>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </React.Fragment>
    )
  }
}
export default AddCompany
