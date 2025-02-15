class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            questions: [],
            mockData: [],
            descripcionIA: ''
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleIAChange = this.handleIAChange.bind(this);
        this.handleIASubmit = this.handleIASubmit.bind(this);
    }

    componentDidMount() {
        fetch('questions.json')
            .then(response => response.json())
            .then(data => this.setState({ questions: data.questions }))
            .catch(error => console.error('Error fetching questions:', error));

        fetch('mock.json')
            .then(response => response.json())
            .then(data => this.setState({ mockData: data.results }))
            .catch(error => console.error('Error fetching mock data:', error));
    }

    handleIAChange(event) {
        this.setState({ descripcionIA: event.target.value });
    }

    handleIASubmit(event) {
        event.preventDefault();
        const descripcion = this.state.descripcionIA;
        fetch('http://localhost:5000/procesarIA', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ descripcion })
        })
        .then(response => response.json())
        .then(data => {
            const json = JSON.stringify(data);
            const encodedJson = encodeURIComponent(json);
            // Redirigir a resultsIA.html en lugar de results.html
            window.location.href = `resultsIA.html?results=${encodedJson}`;
        })
        .catch(error => console.error('Error:', error));
    }

    handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const answers = {};

        this.state.questions.forEach(question => {
            const category = question.category;
            const value = formData.get(`question_${question.id}`);
            if (category && value) {
                answers[category] = parseInt(value, 10);
            }
        });

        fetch('http://localhost:5000/procesar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(answers)
        })
        .then(response => response.json())
        .then(data => {
            const json = JSON.stringify(data);
            const encodedJson = encodeURIComponent(json);
            window.location.href = `results.html?results=${encodedJson}`;
        })
        .catch(error => console.error('Error:', error));
    }

    render() {
        return (
            <div>
                <h1 className="title">Descobreix la teva zona preferida a Tarragona! 🚀</h1>
                <div className="image-container">
                    <img src="./tarragona.jpeg" alt="Tarragona Image" className="background-image" />
                    <div className="grid-overlay">
                        {[...Array(16)].map((_, index) => (
                            <button key={index} className="grid-button">Zona {index + 1}</button>
                        ))}
                    </div>
                </div>

                <div className="ia-search-container">
                    <h2>Descobreix el teu perfil amb IA</h2>
                    <form onSubmit={this.handleIASubmit} className="ia-search-form">
                        <label>Descriu els teus gustos i preferències per a viure a Tarragona:</label>
                        <input
                            type="text"
                            value={this.state.descripcionIA}
                            onChange={this.handleIAChange}
                            placeholder="M'agrada fer esport i tenir natura a prop..."
                            required
                            className="ia-input"
                        />
                        <button type="submit" className="ia-button">Coneix-te amb la nostra IA</button>
                    </form>
                </div>

                <h1 className="title">Emplena el qüestionari perquè et puguem recomanar una zona</h1>
                <form onSubmit={this.handleSubmit} className="questionnaire-form">
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
                    <button type="submit" className="submit-button">Enviar respostes</button>
                </form>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById("root")); 
