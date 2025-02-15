class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            questions: []
        };
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        fetch('questions.json')
            .then(response => response.json())
            .then(data => {
                console.log('Fetched questions:', data.questions);
                this.setState({ questions: data.questions });
            })
            .catch(error => console.error('Error fetching questions:', error));
    }

    handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const answers = {};
        this.state.questions.forEach(question => {
            answers[question.id] = formData.get(`question_${question.id}`);
        });
        const json = JSON.stringify(answers, null, 2);
        console.log('Form JSON:', json);
        // You can send the JSON to a server or process it further here
    }

    render() {
        return (
            <div>
                <div>
                    <h1>Descobreix la teva zona preferida a Tarragona! 🚀</h1>
                    <div className="image-container">
                        <img src="./tarragona.jpeg" alt="Tarragona Image" className="background-image" />
                        <div className="grid-overlay">
                            {[...Array(16)].map((_, index) => (
                                <button key={index} className="grid-button">Zona {index + 1}</button>
                            ))}
                        </div>
                    </div>
                </div>
                <div>
                    <h1>Emplena el cuestionari per que et poguem recomanar una zona</h1>
                    <form onSubmit={this.handleSubmit}>
                        {this.state.questions.map(question => (
                            <div key={question.id} className="form-group">
                                <label>{question.text}</label>
                                <div className="options-container">
                                    {question.scale && question.scale.map(option => (
                                        <div key={option} className="option">
                                            <input type="radio" name={`question_${question.id}`} value={option} required />
                                            <label>{option}</label>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                        <button type="submit">Submit</button>
                    </form>
                </div>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById("root"));