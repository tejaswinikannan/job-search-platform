import JobListing from './JobListing';
import {useState, useEffect} from 'react';
import Spinner from './Spinner';

const JobListings = ({isHome = false, searchQuery = ''}) => {
  const [loading, setLoading] = useState(true);
  const [jobListings, setJobs] = useState([]);

  useEffect( () => {
    const fetchJobs = async() => {
        setLoading(true);
        const fetchurl = searchQuery
          ? `api/jobs/search?query=${encodeURIComponent(searchQuery)}`
          : 'api/jobs/';
        try{
            const response = await fetch(fetchurl);
            if (response.status === 404) {
              setJobs([]);
            } else {
              const data = await response.json();
              setJobs(isHome ? data.slice(0, 3) : data);
            }
          } catch(error) {
              console.log('Error fetching data', error);
          } finally {
            setLoading(false);
          }
        }
        fetchJobs();
  }, [searchQuery, isHome]);

  return (
    <>
      <section className="bg-blue-50 px-4 py-10">
      <div className="container-xl lg:container m-auto">
        <h2 className="text-3xl font-bold text-indigo-500 mb-6 text-center">
          {isHome ? 'Recent Jobs' : 'Browse Jobs'}
        </h2>
        {loading
          ? <Spinner loading={loading}></Spinner>
          : jobListings.length === 0
          ? <p className="text-center text-gray-500">No jobs found matching your search.</p>
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