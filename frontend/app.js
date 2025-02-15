class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            questions: [],
            mockData: []
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

        fetch('mock.json')
            .then(response => response.json())
            .then(data => {
                console.log('Fetched mock data:', data.results);
                this.setState({ mockData: data.results });
            })
            .catch(error => console.error('Error fetching mock data:', error));
    }

    handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const answers = {};

        this.state.questions.forEach(question => {
            const category = question.category; // Asegúrate de que cada pregunta tenga una categoría definida
            const value = formData.get(`question_${question.id}`);
            if (category && value) {
                answers[category] = parseInt(value, 10);
            }
        });

        console.log('Formatted Answers:', answers);

        // Enviar los datos al backend
        fetch('http://localhost:5000/procesar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(answers)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response from backend:', data);
            // Redirigir con los datos obtenidos usando el parámetro "results"
            const json = JSON.stringify(data);
            const encodedJson = encodeURIComponent(json);
            window.location.href = `results.html?results=${encodedJson}`;
        })
        .catch(error => console.error('Error:', error));
    }

    render() {
        return (
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
                <h1>Emplena el qüestionari perquè et puguem recomanar una zona</h1>
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
        );
    }
}

ReactDOM.render(<App />, document.getElementById("root"));
