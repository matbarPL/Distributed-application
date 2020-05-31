import axios from 'axios'

export const register = newUser => {
  return axios
    .post('http://localhost:5000/api/users/register', {
      first_name: newUser.first_name,
      last_name: newUser.last_name,
      email: newUser.email,
      password: newUser.password
    })
    .then(response => {
      console.log('Registered')
    })
}

export const login = user => {
  return axios
    .post('http://localhost:5000/api/users/login', {
      email: user.email,
      password: user.password
    })
    .then(response => {
      localStorage.setItem('usertoken', response.data)
      return response.data
    })
    .catch(err => {
      console.log(err)
    })
}

export const uploadData = formData => {
  return axios
    .post('http://localhost:5000/api/uploadfile', formData)
    .then(response => {
      return response.data
    })
    .catch(err => {
      console.log(err)
    })
}

export const generateTimetable = newMPI => {
  return axios
    .post('http://localhost:5000/api/users/function', {
      number_of_classrooms: newMPI.number_of_classrooms,
      number_of_slaves: newMPI.number_of_slaves,
      max_iteration_number: newMPI.max_iteration_number,
      mutation_probability: newMPI.mutation_probability,
      cross_probability: newMPI.cross_probability,
      number_of_init: newMPI.number_of_init,
      program_timeout: newMPI.program_timeout
    })
    .then(response => {
      return response.data
    })
    .catch(err => {
      console.log(err)
    })
}

export const downloadFile = () => {
  return axios
    .get('http://localhost:5000/api/download')
    .then(response => {
      return response.data
    })
    .catch(err => {
      console.log(err)
    })
}
