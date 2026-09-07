import {Outlet} from 'react-router-dom';
import Navbar from '../components/Navbar';
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// The reason we have nabvar on top of outlet is we want it to be shown on all pages

const MainLayout = () => {
  return (
    <>
        <Navbar/>
        <Outlet/>
        <ToastContainer/>
    </>
  )
}

export default MainLayout