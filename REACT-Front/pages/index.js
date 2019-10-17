import { Header, Button, Container } from 'semantic-ui-react';
import '../.semantic/dist/semantic.min.css';

const Home = () => (
  <Container>
    <div>
      <Header as="h2">Next.js + Semantic UI!</Header>
    </div>
    <div>
      <Button primary>Primary</Button>
      <Button secondary>Secondary</Button>
    </div>
  </Container>
);
export default Home;
