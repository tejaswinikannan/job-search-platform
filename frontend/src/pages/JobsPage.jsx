import React, { useState } from 'react'
import JobListings from '../components/JobListings'

const JobsPage = () => {
  const [searchText, setSearchText] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchQuery(searchText.trim());
  };

  return (
    <>
        <section className="bg-indigo-50 px-4 py-6">
          <div className="container-xl lg:container m-auto">
            <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                placeholder="Search jobs in plain English, e.g. 'remote SQL jobs in Boston'"
                className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
              <button
                type="submit"
                className="bg-indigo-500 hover:bg-indigo-600 text-white px-6 py-2 rounded-lg"
              >
                Search
              </button>
            </form>
          </div>
        </section>
        <JobListings searchQuery={searchQuery}/>
    </>

  )
}

export default JobsPage