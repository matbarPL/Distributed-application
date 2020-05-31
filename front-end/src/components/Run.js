import React, { Component } from 'react'
import axios from 'axios'
//import jwt_decode from 'jwt-decode'
import { generateTimetable } from './UserFunctions'
import { uploadData } from './UserFunctions'
//import { downloadFile } from './UserFunctions'

class Run extends Component {
  constructor() {
    super()
    this.state = {
      selectedFile: null,
      isSelectedFileUploaded: 1,
      init_number: 16,
      number_of_classrooms: 4,
      number_of_slaves: 0,
      max_iteration_number: 2000,
      mutation_probability: 100,
      cross_probability: 0,
      time: 0,
      start: 0,
      isOn: false,
      tryGenerateIsOn: 0,
      isTimetableReady: 0,
      error: ''
    }

    this.onChange = this.onChange.bind(this)
    this.startTimer = this.startTimer.bind(this)
    this.stopTimer = this.stopTimer.bind(this)
    this.tryGenerate = this.tryGenerate.bind(this)
  }

  componentDidUpdate(){
    setTimeout(() => this.setState({error:''}), 5000);
  }

  startTimer() {
    this.setState({
      time: this.state.time,
      start: Date.now() - this.state.time,
      isOn: true
    })
    this.timer = setInterval(() => this.setState({
      time: Date.now() - this.state.start
    }), 1);
  }
  stopTimer() {
    this.setState({isOn: false})
    clearInterval(this.timer)
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value })
  }

    onFileChange = event => {
      // Update the state
      this.setState({ selectedFile: event.target.files[0] });
    };

    fileData = () => {
      if (this.state.selectedFile) {
        return (
          <div><br /><b>File Details:</b>
          <p>File Name: {this.state.selectedFile.name}</p>
          <p>File Type: {this.state.selectedFile.type}</p>
          </div>
        );
      } else {
        return (
          <div><br /> <h5>Choose before pressing the Upload button</h5></div>
        );
      }
    };

    // On file upload (click the upload button)
    onFileUpload = () => {
       const formData = new FormData();
       formData.append(
         "file",
         this.state.selectedFile,
         this.state.selectedFile.name
       );
       console.log(this.state.selectedFile);

       uploadData(formData).then(res => {
         if (!res.error) {
           this.setState({
               isSelectedFileUploaded: 1
           })
         }
         else {
           this.setState({
           error: res.error
         });
         }
       })
     };


    showSettings = () =>  {
      if(this.state.isSelectedFileUploaded === 1 && this.state.tryGenerateIsOn === 0) {
        return (
          <div className="container">
            <div className="row">
              <div className="col-md-6 mt-5 mx-auto">
                <form noValidate onSubmit={this.tryGenerate}>
                  <div className="form-group">
                     <label htmlFor="init_number">Number of init population</label>
                     <input type="number" min="4" max="20" className="form-control" name="init_number" placeholder="Enter init population"
                       value={this.state.init_number}
                       onChange={this.onChange}/>
                   </div>
                   <div className="form-group">
                     <label htmlFor="number_of_classrooms">Number of classrooms</label>
                     <input type="number" min="4" max="20" className="form-control" name="number_of_classrooms" placeholder="Enter number of classrooms"
                       value={this.state.number_of_classrooms}
                       onChange={this.onChange}/>
                   </div>
                   <div className="form-group">
                     <label htmlFor="mutation_probability">Mutation probability</label>
                     <input type="number" min="80" max="100" className="form-control" name="mutation_probability" placeholder="Enter mutation probability"
                       value={this.state.mutation_probability}
                       onChange={this.onChange}/>
                   </div>
                   <div className="form-group">
                     <label htmlFor="cross_probability">Cross probability</label>
                     <input type="number" min="0" max="100" className="form-control" name="cross_probability" placeholder="Enter cross probability"
                       value={this.state.cross_probability}
                       onChange={this.onChange}/>
                   </div>
                     <div className="form-group">
                       <label htmlFor="number_of_slaves">Number of slaves</label>
                       <input type="number" min="0" max="2" className="form-control" name="number_of_slaves" placeholder="Enter number of slaves"
                         value={this.state.number_of_slaves}
                         onChange={this.onChange}/>
                     </div>
                     <div className="form-group">
                       <label htmlFor="max_iteration_number">Maximum iteration number</label>
                       <input type="number" min="1000" max="2000" className="form-control" name="max_iteration_number" placeholder="Enter max iteration number"
                         value={this.state.max_iteration_number}
                         onChange={this.onChange}/>
                     </div>
                     <button type="submit" className="btn btn-lg btn-primary btn-block">
                       Generate!
                     </button>
                </form>
              </div>
            </div>
        </div>
        );
      }
    }

    waitForTheFile = () => {
      if (this.state.time !== 0 && this.state.isOn) {
        return (
          <h4> (wait for the file) </h4>
        );
      }
    };

   timerIsOn = () => {
     if (this.state.tryGenerateIsOn !== 0) {
       return (
           <div>
             <h3>timer: {this.state.time} ms </h3>
             {this.waitForTheFile()}
             {this.generateSuccessed()}
           </div>
         );
       }
   };

    tryGenerate = (e) => {
        this.setState({
            tryGenerateIsOn: 1
        })
        e.preventDefault()

        const newMPI = {
          init_number: this.state.init_number,
          number_of_classrooms: this.state.number_of_classrooms,
          number_of_slaves: this.state.number_of_slaves,
          max_iteration_number: this.state.max_iteration_number,
          mutation_probability: this.state.mutation_probability,
          cross_probability: this.state.cross_probability,
          token: localStorage.usertoken
        }
        
        this.startTimer()
            generateTimetable(newMPI).then(res => {
              if (!res.error) {
                this.stopTimer()
                console.log(res);
                 this.setState({
                   isTimetableReady: 1
               });
               }
               else {
                 this.stopTimer()
                 this.setState({
                   error: res.error
               });
               console.log(res.error);
               }
            })
      }

    downloadFile = () => {
      axios.get("/api/download")
      /*downloadFile().then(res => {
          if (res.error) {
              this.setState({
                error: res.error
            });
          }
        })*/
     };

     generateSuccessed = () => {
       if (this.state.isTimetableReady === 1) {
         return (
           <div>
           {this.downloadFile()}
           <a href="http://localhost:3000/api/download">
             <button>Download</button>
           </a>
           </div>
         );
       }
     };

  render() {
    return (
      <div className="container">
        <div className="jumbotron mt-5">
          <div className="col-sm-8 mx-auto">
            <h1 className="text-center">Timetable generator</h1>
          </div>
        </div>
        <span className="error">{this.state.error}</span>
        <h3>
         Upload your data file:
        </h3>
           <div>
               <input type="file" onChange={this.onFileChange} name="image"/>
               <button onClick={this.onFileUpload}>
                 Upload!
               </button>
           </div>

         {this.fileData()}
         {this.showSettings()}
         {this.timerIsOn()}


  </div>
    )
  }
}

export default Run
