import React from 'react'

import { 
    Card,
    Table,
    Subtitle1
} from 'ui-neumorphism'

function createItem(name, contributions) {
    return { name, contributions }
  }

const headers = [
    {
      text: 'Name',
      align: 'left',
      value: 'name'
    },
    { text: 'Contributions', align: 'left', value: 'contributions' }
]

const items = [
    createItem('Dr. Jason Jaskolka', 'Professor Jaskolka acted as our mentor for the duration of the project and is the best professor ever. Thanks professor!'),
    createItem('Tony Abou Zeidan', 'Tony contributed to the project as the spokesman and as one of the main software developers. Tony participated in the development of the front-end, and in the formulation of the detection/parsing algorithms. Thanks Tony!'),
    createItem('Anthony Dooley', 'Anthony contributed to the project as one of the main software developers. Anthony primarily focused on and contributed to the development of the detection and parsing algorithms. Thanks Anthony!'),
    createItem('Shaopeng Liu', 'Anthony contributed to the project as one of the main software developers. Shaopeng primarily focused on and contributed to the front-end and back-end development as well as development of the detection and parsing algorithms. Thanks Shaopeng!'),
    createItem('Ethan Chase', 'Ethan contributed to the project as one of the main software developers. Ethan primarily focused on and contributed to the development of the detection and parsing algorithms. Thanks Ethan!'),
  ]

class CreditsForm extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
        <Card
          className='mt-12'
          title="Evase Project Credits"
          subtitle={
            <Subtitle1>
              Thank you to all of those who helped with this project! It was a blast working with all of you.
            </Subtitle1>
          }
          content={
            <Card flat className='fill-width px-6 mt-6'>
              <Table inset items={items} headers={headers} />
            </Card>
          }
        />);
    }
}

export default CreditsForm;