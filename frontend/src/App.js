import React, { Component } from "react";
import Select from 'react-select'
import "./App.css";
import "bootstrap/dist/css/bootstrap.css";
import axios from 'axios'
import Spinner from "./Spinner";

const options = [
  { value: 'Active', label: 'Active' },
  { value: 'Blacklisted', label: 'Blacklisted' },
  { value: 'Responded', label: 'Responded' },
  { value: 'Invalid', label: 'Invalid' },
  { value: 'Bounced', label: 'Bounced' },
  { value: 'Opt-Out', label: 'Opt-Out' } 
];

class App extends Component {
  state = {
    data: [],
    selectedOption: null,
  };

  

  async componentDidMount() {
     this.pull_dB()
  }
  fetchData = () => {
    fetch("/submit", {
      method: "GET",
      dataType: "JSON",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
    })
      .then((resp) => {
        return resp.json();
      })
      .then((values) => {
        this.pull_dB()
        console.log(this.state);
      })
      .catch((error) => {
        console.log(error, "catch the hoop");
      });
  };

  pushHub = () => {

    fetch("/push_hub", {
      method: "GET",
      dataType: "JSON",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
    })
      .then((resp) => {
        return resp.json();
      })
      .then((values) => {
        console.log(values);
      })
      .catch((error) => {
        console.log(error, "catch the hoop");
      });

    
  };

  pullHub = () => {

    fetch("/hub_pull", {
      method: "GET",
      dataType: "JSON",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
    })
      .then((resp) => {
        return resp.json();
      })
      .then((hub_pull) => {
        console.log(hub_pull);
      })
      .catch((error) => {
        console.log(error, "catch the hoop");
      });

    
  };

  pull_dB = () =>{
    fetch("/pull_dB", {
      method: "GET",
      dataType: "JSON",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
    })
      .then((resp) => {
        return resp.json();
      })
      .then((pulled_Data) => {
        this.setState({ data: pulled_Data });
        console.log(pulled_Data);
      })
      .catch((error) => {
        console.log(error, "catch the hoop");
      });
  };

  handleChange = (selectedOption) => {
    this.setState({ selectedOption });
    console.log(`Option selected:`, selectedOption);
  }

  onUpdate = (id,update_value) => {

    console.log("Id", id, "Sel", update_value.value )
    axios.put(`/update/${id}`, update_value
    ).then( response=>{
      console.log('The returned', response)
      window.location.reload(false);
      })
    .catch(error => {
       console.log(error)
     })
     alert('The Email Reliability Status Was Updated :(') 

  }
   
  onWoodpecker =() =>{
    fetch("/push_woodpecker", {
      method: "GET",
      dataType: "JSON",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
    })
      .then((resp) => {
        return resp.json();
      })
      .then((hub_pull) => {
        console.log(hub_pull);
      })
      .catch((error) => {
        console.log(error, "catch the hoop");
      });
  }


  render() {
    const { data } = this.state;
    const { selectedOption } = this.state;
    return (
      <div className="App">
        <div className="container">
          <div className="row rows">
            <div className="col">
              <button onClick={this.fetchData} className="btn btn-primary">
                Load Data From Sheet
              </button>
              <div className="divider"/>
              <button onClick={this.pushHub} className="btn btn-primary">Push Data to Hubspot</button>
            </div>
          </div>
          <hr/>
          <div className="row rows">
            <div className="col">
              <button onClick={this.pullHub} className="btn btn-primary">
                Pull Data From Hubspot
              </button>
              <div className="divider"/>
              <button onClick={this.onWoodpecker} className="btn btn-primary">
                Push Data to Woodpecker
              </button>
            </div>
          </div>
          <hr/>
          <div id="cont">
            <table className="table table-straight">
              <thead className="thead-inverse">
                <tr>
                  <th>First Name</th>
                  <th>Last Name</th>
                  <th>Email</th>
                  <th>Job Title Full</th>
                  <th>Job Title</th>
                  <th>City</th>
                  <th>Country</th>
                  <th>Company</th>
                  <th>Company Website</th>
                  <th>LinkedIn</th>
                  <th>Company Industry</th>
                  <th>Company Founde</th>
                  <th>Company Size</th>
                  <th>Company LinkedIn</th>
                  <th>Company Headquaters</th>
                  <th>Email Reliability Status</th>
                  <th >Receiving Mail Server</th>
                  <th>Kind</th>
                  <th>Tag</th>
                  <th>Month</th>
                  <th className="Sel">Select WP Options</th>
                </tr>
              </thead>
              <tbody>
                {data.map((passed_data) => (
                  <tr key={passed_data.id}>
                    <td>{passed_data.first_name}</td>
                    <td>{passed_data.last_name}</td>
                    <td>{passed_data.email}</td>
                    <td>{passed_data.job_title_full}</td>
                    <td>{passed_data.job_title}</td>
                    <td>{passed_data.city}</td>
                    <td>{passed_data.country}</td>
                    <td>{passed_data.company}</td>
                    <td>{passed_data.company_website}</td>
                    <td>{passed_data.linkedin}</td>
                    <td>{passed_data.company_industry}</td>
                    <td>{passed_data.company_founded}</td>
                    <td>{passed_data.company_size}</td>
                    <td>{passed_data.company_linkedin}</td>
                    <td>{passed_data.company_headquaters}</td>
                    <td>{passed_data.email_reliability_status}</td>
                    <td>{passed_data.receiving_mail_server}</td>
                    <td>{passed_data.kind}</td>
                    <td>{passed_data.tag}</td>
                    <td>{passed_data.month}</td>
                    <td><Select
                    onChange={this.handleChange}
                     options = {options} 
                     autoFocus={true} /></td>
                    <td>
                      <button onClick={this.onUpdate.bind(this, passed_data.id, selectedOption)} className="btn btn-success">Update</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
