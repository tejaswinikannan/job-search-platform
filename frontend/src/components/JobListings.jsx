import JobListing from './JobListing';
import {useState, useEffect} from 'react';
import Spinner from './Spinner';

const JobListings = ({isHome = false}) => {
  const [loading, setLoading] = useState(true);
  const [jobListings, setJobs] = useState([]);
  
  useEffect( () => {
    const fetchJobs = async() => {
        const fetchurl = 'api/jobs/';
        try{
            const response = await fetch(fetchurl);
            const data = await response.json()
            setJobs(isHome ? data.slice(0, 3) : data);
          } catch(error) {
              console.log('Error fetching data', error);
          } finally {
            setLoading(false);
          }
        }
        fetchJobs();
  }, []);

  return (
    <>
      <section className="bg-blue-50 px-4 py-10">
      <div className="container-xl lg:container m-auto">
        <h2 className="text-3xl font-bold text-indigo-500 mb-6 text-center">
          {isHome ? 'Recent Jobs' : 'Browse Jobs'}
        </h2>
        {loading 
          ? <Spinner loading={loading}></Spinner>
          : 
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {jobListings.map(job=>(
              <JobListing key={job.id} job={job}/>
            ))}
        </div>
        }
      </div>
    </section>
    </>
  )
}

export default JobListings