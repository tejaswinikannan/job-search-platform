import { createBrowserRouter,RouterProvider } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MainLayout from './layouts/MainLayout';
import JobsPage from './pages/JobsPage';
import NotFound from './pages/NotFound';
import JobPage, {JobLoader} from './pages/JobPage';
import AddJobPage from './pages/AddJobPage';
import EditJobPage from './pages/EditJobPage';

const App = () => {
  //Add Job
  const addJob = async(newJob) => {
    const res = await fetch('/api/jobs/', {
      method: 'POST',
      headers: {
        'Content-Type':'application/json'
      },
      body: JSON.stringify(newJob)
    });
    return;
  }
  //Delete Job
  const deleteJob = async(id) => {
    const res = await fetch(`/api/jobs/${id}`, {
      method: 'DELETE'
    });
    return;
  }

  //Update Job
  const updateJob = async(updatedJob) => {
    const res = await fetch(`/api/jobs/${updatedJob.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type':'application/json'
      },
      body: JSON.stringify(updatedJob)
    });
    return;
  }

  
  const router = createBrowserRouter([
    {
      path: "/",
      element: <MainLayout/>,
      children:[
        {
          index: true, //default child page
          element: <HomePage/>,
        },{
          path: "/jobs",
          element: <JobsPage/>,
        },{
          path: "/jobs/:id", 
          element: <JobPage deleteJob={deleteJob}/>,
          loader: JobLoader,
        },{
          path: "/add-job",
          element: <AddJobPage addJobSubmit={addJob}/>
        },{
          path: "/edit-job/:id",
          element: <EditJobPage updateJobSubmit={updateJob}/>,
          loader: JobLoader,
        }, {
          path:"*",
          element:<NotFound/> 
        }
      ]
    },
  ]);
  return (
    <RouterProvider router={router}/>
  )
}


export default App