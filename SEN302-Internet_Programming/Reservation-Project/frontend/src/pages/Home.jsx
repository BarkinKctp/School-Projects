import '../css/Home.css';

export function Home() {
    return (
        <>
            <div className="home-page">
                <h1>Welcome</h1>
                <p className="subtitle">User Management System</p>
                
                <div className="gears-container">
                    <div className="gear gear-1">⚙</div>
                    <div className="gear gear-2">⚙</div>
                    <div className="gear gear-3">⚙</div>
                </div>
                
                <p className="description">Manage your users with ease</p>
            </div>

            <section className="about-section">
                <div className="about-content">
                    <div className="features">
                        <div className="feature">
                            <span className="feature-icon">📝</span>
                            <h3>Create</h3>
                            <p>Add new users to the database</p>
                        </div>
                        <div className="feature">
                            <span className="feature-icon">📖</span>
                            <h3>Read</h3>
                            <p>View all users in the system</p>
                        </div>
                        <div className="feature">
                            <span className="feature-icon">✏️</span>
                            <h3>Update</h3>
                            <p>Edit existing user information</p>
                        </div>
                        <div className="feature">
                            <span className="feature-icon">🗑️</span>
                            <h3>Delete</h3>
                            <p>Remove users from the database</p>
                        </div>
                    </div>
                    <div className="about-text">
                        <h2>About This Project</h2>
                        <p>
                            This is a full-stack CRUD application built with React and Node.js. 
                            It demonstrates user management capabilities including creating, reading, 
                            updating, and deleting user records.
                        </p>
                        <p>
                            The frontend uses React with React Router for navigation, while the 
                            backend is powered by Node.js with Express and a SQL database for 
                            persistent storage.
                        </p>
                    </div>
                </div>
            </section>

            <footer className="footer">
                <div className="footer-content">
                    <h3>Connect With Me</h3>
                    <p>
                        Built as a learning project for React & Node.js<br/>
                        Full-stack CRUD application with modern web technologies
                    </p>
                    <div className="footer-links">
                        <a href="https://github.com/BarkinKctp" target="_blank" rel="noopener noreferrer">GitHub</a>
                        <a href="https://www.linkedin.com/in/barkin-kocatepe-6a43922a2/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
                    </div>
                    
                </div>
            </footer>
        </>
    );
}
