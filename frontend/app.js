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
            answers[question.id] = formData.get(`question_${question.id}`);
        });

        // Use the mock data
        const mockData = this.state.mockData;
        console.log('Mock Data:', mockData);

        // Combine form answers with mock data
        const combinedData = {
            mockData: mockData
        };

        const json = JSON.stringify(combinedData);
        const encodedJson = encodeURIComponent(json);
        window.location.href = `results.html?answers=${encodedJson}`;
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