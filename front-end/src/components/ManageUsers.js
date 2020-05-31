import React from "react";
import { Container, Row, Col, Card, CardHeader, CardBody, Button} from "shards-react";
import axios from 'axios'
import { Redirect } from "react-router-dom";

class ManageUsers extends React.Component {
  constructor(props){
    super(props);
    this.deleteUser = this.deleteUser.bind(this);
    this.state = {
      users: [],
      chosenId: 1
    }
  }

  componentDidMount(){
    this.getDefaultUsersData();
  }

  async getDefaultUsersData(){
    const response = await axios.get('api/users/get')
    this.setState({
      users: response.data
      });
  }

  deleteUser(event, userId){
    axios.post('api/users/delete', {
        id:userId
    })
  }

  render(){
      return(
        <Container fluid className="main-content-container px-4">
            <Row>
              <Col>
                <Card small className="mb-4">
                  <CardHeader className="border-bottom">
                    <h6 className="m-0"></h6>
                  </CardHeader>
                  <CardBody className="p-0 pb-3">
                    <table className="table mb-0">
                      <thead className="bg-light">
                        <tr>
                          <th scope="col" className="border-0" >                          
                            id
                          </th>
                          <th scope="col" className="border-0" >
                            first_name
                          </th>
                          <th scope="col" className="border-0" >
                            last_name
                          </th>
                          <th scope="col" className="border-0" >
                            email
                          </th>
                          <th scope="col" className="border-0" >
                            admin
                          </th>
                          <th scope="col" className="border-0" >
                            action
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {this.state.users.map(user => (
                          <tr key={user.id}>
                            <td>{user.id}</td>
                            <td>{user.first_name}</td>
                            <td>{user.last_name}</td>
                            <td>{user.email}</td>
                            <td>{user.admin.toString()}</td>
                            <td>
                                <Button onClick={(event) => {this.deleteUser(event, user.id)}}>
                                    Delete
                                </Button>
                            </td>
                          </tr>
                          ))}
                      </tbody>
                    </table>
                  </CardBody>
                </Card>
              </Col>
            </Row>
        </Container>
      )
    }
};

export default ManageUsers;
