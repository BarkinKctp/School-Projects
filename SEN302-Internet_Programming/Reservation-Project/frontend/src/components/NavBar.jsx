import { Link } from 'react-router-dom';
import '../css/NavBar.css';

export function NavBar() {
    return (
        <nav className="nav-bar">
            <div className="nav-title">
                <Link to="/">
                    <span className="home-icon">👤</span>
                    User Management
                </Link>
            </div>
            <div className="nav-links">
                <Link to="/">Home</Link>
                <Link to="/Data">Data</Link>
            </div>
        </nav>
    );
}  





