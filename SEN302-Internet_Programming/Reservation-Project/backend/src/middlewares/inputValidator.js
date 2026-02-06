import joi from 'joi';

const userSchema = joi.object({
    username: joi.string().alphanum().min(3).max(30).required(),
    email: joi.string().email().required(),
});

const validateUser = (req, res, next) => {
    const { error } = userSchema.validate(req.body);
    if (error) {
        return res.status(400).json({
            status: 400,
            message: 'Invalid input data',
            details: error.details.map(detail => detail.message)
        });
    }
    next();
}

export default validateUser;