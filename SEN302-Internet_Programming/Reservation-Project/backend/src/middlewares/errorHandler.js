
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);

    // Handle PostgreSQL unique constraint violation
    if (err.code === '23505') {
        return res.status(409).json({
            status: 409,
            message: 'Email already exists',
            error: err.message
        });
    }

    res.status(500).json({
        status: 500,
        message: 'Internal Server Error',
        error: err.message
    });
};

export default errorHandler;


