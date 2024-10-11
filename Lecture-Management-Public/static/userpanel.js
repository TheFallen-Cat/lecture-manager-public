const degreeCheckbox = document.getElementById("degree_checkbox");
const juniorCheckbox = document.getElementById("junior_checkbox");
const classField = document.getElementById("main_class");
const subjectField = document.getElementById("subject");

const degreeChoices = ["FYBSc", "SYBsc", "TYBsc", "FYBCom", "SYBCom", "TYBCom"];
const juniorChoices = [
  "11th Science 1",
  "11th Science 2",
  "11th Science 3",
  "12th Science 1",
  "12th Science 2",
  "12th Science 3",
];

const degreeSubjects = [
  "Numerical Analysis",
  "Computer Programming & System Analysis-1",
  "IT for Business",
  "Computer Systems and applications-1",
  "Real Analysis",
  "Metric Space",
  "Discrete Mathematics",
  "Calculus 3",
];
const juniorSubjects = ["Mathematics (Jr)"];

function updateSelectOptions() {
  const degreeChecked = degreeCheckbox.checked;
  const juniorChecked = juniorCheckbox.checked;

  classField.innerHTML = "";
  subjectField.innerHTML = "";

  let classChoices = [];
  let subjectChoices = [];
  if (degreeChecked) {
    classChoices = classChoices.concat(degreeChoices);
    subjectChoices = subjectChoices.concat(degreeSubjects);
  } else if (juniorChecked) {
    classChoices = classChoices.concat(juniorChoices);
    subjectChoices = subjectChoices.concat(juniorSubjects);
  }

  classChoices.forEach((choice) => {
    const option = new Option(choice, choice);
    classField.appendChild(option);
  });

  subjectChoices.forEach((choice) => {
    const option = new Option(choice, choice);
    subjectField.appendChild(option);
  });
}

degreeCheckbox.addEventListener("change", updateSelectOptions);
juniorCheckbox.addEventListener("change", updateSelectOptions);

updateSelectOptions();
