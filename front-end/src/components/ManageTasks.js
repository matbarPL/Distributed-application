import React from "react";
import { Container, Row, Col, Card, CardHeader, CardBody, Button} from "shards-react";
import axios from 'axios'
import jwt_decode from 'jwt-decode'

class ManageTasks extends React.Component {
  constructor(props){
    super(props);
    this.deleteTask = this.deleteTask.bind(this);
    this.state = {
      tasks: []
    }
  }

  componentDidMount(){
    this.getDefaultTasksData();
  }

  async getDefaultTasksData(){
    const token = localStorage.usertoken
    const decoded = jwt_decode(token)
    const userId = decoded.identity.id

    await axios.get('api/tasks/'+userId.toString())
    .then(response=>{ 
      this.setState({
        tasks: response.data
      });
    })
  }

  async deleteTask(event, taskId){
    const token = localStorage.usertoken
    const decoded = jwt_decode(token)
    const userId = decoded.identity.id

    await axios.post('api/tasks/delete', {
        task_id:taskId,
        user_id:userId
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
                            init population nr
                          </th>
                          <th scope="col" className="border-0" >
                            nr classrooms
                          </th>
                          <th scope="col" className="border-0" >
                            nr slaves
                          </th>
                          <th scope="col" className="border-0" >
                            max iterations nr
                          </th>
                          <th scope="col" className="border-0" >
                            mutation probability
                          </th>
                          <th scope="col" className="border-0" >
                            cross probability
                          </th>
                          <th scope="col" className="border-0" >
                            creation time
                          </th>
                          <th scope="col" className="border-0" >
                            Action
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {this.state.tasks.map(task => (
                          <tr key={task.id}>
                            <td>{task.id}</td>
                            <td>{task.init_number}</td>
                            <td>{task.number_of_classrooms}</td>
                            <td>{task.number_of_slaves}</td>
                            <td>{task.max_iteration_number}</td>
                            <td>{task.mutation_probability}</td>
                            <td>{task.cross_probability}</td>
                            <td>{task.creation_time}</td>
                            <td>
                                <Button onClick={(event) => {this.deleteTask(event, task.id)}}>
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

export default ManageTasks;
