// Google Apps Script for creating STH MCQ Quiz
// To use: Create a new Google Form, copy this script to Script Editor, and run createSTHQuiz()

function createSTHQuiz() {
  // Create a new Google Form
  var form = FormApp.create('Soil Transmitted Diseases (STH) Quiz - MBBS 3rd Year');

  // Set as quiz mode first
  form.setIsQuiz(true);

  // Add title and description
  form.setDescription('Multiple Choice Questions on Soil Transmitted Diseases for MBBS 3rd Year students. Total Questions: 20');

  // Question 1: Basic Definition
  var item1 = form.addMultipleChoiceItem();
  item1.setTitle('1. Which of the following organisms are considered Soil Transmitted Helminths (STH)?')
    .setChoices([
      item1.createChoice('Entamoeba histolytica, Giardia lamblia, Cryptosporidium', false),
      item1.createChoice('Ascaris lumbricoides, Trichuris trichiura, Necator americanus', true),
      item1.createChoice('Wuchereria bancrofti, Brugia malayi, Mansonella ozzardi', false),
      item1.createChoice('Strongyloides stercoralis, Schistosoma mansoni, Taenia solium', false)
    ])
    .setPoints(1);
  item1.setRequired(true);

  // Question 2: Global Burden
  var item2 = form.addMultipleChoiceItem();
  item2.setTitle('2. According to WHO estimates (2023), approximately how many people are infected with STH globally?')
    .setChoices([
      item2.createChoice('500 million', false),
      item2.createChoice('1 b illion', false),
      item2.createChoice('1.5 billion', true),
      item2.createChoice('2.1 billion', false)
    ])
    .setPoints(1);
  item2.setRequired(true);

  // Question 3: Transmission
  var item3 = form.addMultipleChoiceItem();
  item3.setTitle('3. Which STH is transmitted through percutaneous penetration of the skin?')
    .setChoices([
      item3.createChoice('Ascaris lumbricoides', false),
      item3.createChoice('Trichuris trichiura', false),
      item3.createChoice('Hookworms (Necator americanus)', true),
      item3.createChoice('All STH use this route', false)
    ])
    .setPoints(1);
  item3.setRequired(true);

  // Question 4: Epidemiology
  var item4 = form.addMultipleChoiceItem();
  item4.setTitle('4. Which continent has the highest burden of STH infections?')
    .setChoices([
      item4.createChoice('Asia', false),
      item4.createChoice('Africa', true),
      item4.createChoice('South America', false),
      item4.createChoice('Europe', false)
    ])
    .setPoints(1);
  item4.setRequired(true);

  // Question 5: Life Cycle
  var item5 = form.addMultipleChoiceItem();
  item5.setTitle('5. What is the Primary infective stage for Ascaris lumbricoides?')
    .setChoices([
      item5.createChoice('Adult worm', false),
      item5.createChoice('Embryonated egg', true),
      item5.createChoice('Rhabditiform larva', false),
      item5.createChoice('Filariform larva', false)
    ])
    .setPoints(1);
  item5.setRequired(true);

  // Question 6: Clinical Features
  var item6 = form.addMultipleChoiceItem();
  item6.setTitle('6. Which clinical syndrome is associated with the pulmonary phase of Ascaris migration?')
    .setChoices([
      item6.createChoice('Hemoptysis', false),
      item6.createChoice('Loeffler\'s syndrome', true),
      item6.createChoice('Ground itch', false),
      item6.createChoice('Rectal prolapse', false)
    ])
    .setPoints(1);
  item6.setRequired(true);

  // Question 7: Complications
  var item7 = form.addMultipleChoiceItem();
  item7.setTitle('7. Rectal prolapse is most commonly associated with which STH?')
    .setChoices([
      item7.createChoice('Ascaris lumbricoides', false),
      item7.createChoice('Trichuris trichiura', true),
      item7.createChoice('Ancylostoma duodenale', false),
      item7.createChoice('Necator americanus', false)
    ])
    .setPoints(1);
  item7.setRequired(true);

  // Question 8: Diagnosis
  var item8 = form.addMultipleChoiceItem();
  item8.setTitle('8. What is the most common method for diagnosing STH infections?')
    .setChoices([
      item8.createChoice('Blood culture', false),
      item8.createChoice('Urine analysis', false),
      item8.createChoice('Stool examination', true),
      item8.createChoice('Skin biopsy', false)
    ])
    .setPoints(1);
  item8.setRequired(true);

  // Question 9: Egg Identification
  var item9 = form.addMultipleChoiceItem();
  item9.setTitle('9. Which STH egg has a characteristic barrel shape with bipolar plugs?')
    .setChoices([
      item9.createChoice('Ascaris lumbricoides', false),
      item9.createChoice('Trichuris trichiura', true),
      item9.createChoice('Hookworm', false),
      item9.createChoice('Strongyloides', false)
    ])
    .setPoints(1);
  item9.setRequired(true);

  // Question 10: Treatment
  var item10 = form.addMultipleChoiceItem();
  item10.setTitle('10. What is the standard single dose treatment for STH?')
    .setChoices([
      item10.createChoice('400 mg Albendazole', false),
      item10.createChoice('300 mg Mebendazole', false),
      item10.createChoice('10 mg/kg Pyrantel pamoate', false),
      item10.createChoice('All of the above have equivalent efficacy', true)
    ])
    .setPoints(1);
  item10.setRequired(true);

  // Question 11: Special Populations
  var item11 = form.addMultipleChoiceItem();
  item11.setTitle('11. Which anthelmintic drug is considered safest for use in the first trimester of pregnancy?')
    .setChoices([
      item11.createChoice('Albendazole', false),
      item11.createChoice('Mebendazole', false),
      item11.createChoice('Pyrantel pamoate', true),
      item11.createChoice('Levamisole', false)
    ])
    .setPoints(1);
  item11.setRequired(true);

  // Question 12: Prevention
  var item12 = form.addMultipleChoiceItem();
  item12.setTitle('12. Which of the following is the cornerstone of STH control programs?')
    .setChoices([
      item12.createChoice('Sanitation improvement', false),
      item12.createChoice('Mass drug administration', true),
      item12.createChoice('Health education', false),
      item12.createChoice('Water purification', false)
    ])
    .setPoints(1);
  item12.setRequired(true);

  // Question 13: WHO Classification
  var item13 = form.addMultipleChoiceItem();
  item13.setTitle('13. According to WHO, what prevalence threshold requires universal treatment for STH?')
    .setChoices([
      item13.createChoice('Less than 5%', false),
      item13.createChoice('20-50%', false),
      item13.createChoice('Greater than 50%', true),
      item13.createChoice('Greater than 75%', false)
    ])
    .setPoints(1);
  item13.setRequired(true);

  // Question 14: Indian Context
  var item14 = form.addMultipleChoiceItem();
  item14.setTitle('14. Approximately how many cases of STH are estimated in India?')
    .setChoices([
      item14.createChoice('50 million', false),
      item14.createChoice('100 million', false),
      item14.createChoice('225 million', true),
      item14.createChoice('300 million', false)
    ])
    .setPoints(1);
  item14.setRequired(true);

  // Question 15: Risk Factors
  var item15 = form.addMultipleChoiceItem();
  item15.setTitle('15. Which of the following is NOT a major risk factor for STH infection?')
    .setChoices([
      item15.createChoice('Open defecation', false),
      item15.createChoice('Consumption of raw vegetables', false),
      item15.createChoice('Walking barefoot', false),
      item15.createChoice('Air pollution', true)
    ])
    .setPoints(1);
  item15.setRequired(true);

  // Question 16: Complications
  var item16 = form.addMultipleChoiceItem();
  item16.setTitle('16. Which STH is most commonly associated with severe iron deficiency anemia?')
    .setChoices([
      item16.createChoice('Ascaris lumbricoides', false),
      item16.createChoice('Trichuris trichiura', false),
      item16.createChoice('Hookworms', true),
      item16.createChoice('Enterobius vermicularis', false)
    ])
    .setPoints(1);
  item16.setRequired(true);

  // Question 17: Diagnosis Technique
  var item17 = form.addMultipleChoiceItem();
  item17.setTitle('17. What is the WHO recommended method for diagnosing STH infections in field settings?')
    .setChoices([
      item17.createChoice('Direct smear', false),
      item17.createChoice('Kato-Katz technique', true),
      item17.createChoice('Harada-Mori tube', false),
      item17.createChoice('Multiplex PCR', false)
    ])
    .setPoints(1);
  item17.setRequired(true);

  // Question 18: Life Cycle Duration
  var item18 = form.addMultipleChoiceItem();
  item18.setTitle('18. How long does it take for hookworm eggs to develop into infective larvae in the environment?')
    .setChoices([
      item18.createChoice('1-2 days', false),
      item18.createChoice('5-8 days', true),
      item18.createChoice('2-3 weeks', false),
      item18.createChoice('1-2 months', false)
    ])
    .setPoints(1);
  item18.setRequired(true);

  // Question 19: Public Health
  var item19 = form.addMultipleChoiceItem();
  item19.setTitle('19. Which Sustainable Development Goal directly targets the elimination of neglected tropical diseases including STH?')
    .setChoices([
      item19.createChoice('SDG 2 (Zero Hunger)', false),
      item19.createChoice('SDG 3 (Good Health and Well-being)', true),
      item19.createChoice('SDG 6 (Clean Water and Sanitation)', false),
      item19.createChoice('SDG 7 (Affordable and Clean Energy)', false)
    ])
    .setPoints(1);
  item19.setRequired(true);

  // Question 20: Control Strategy
  var item20 = form.addMultipleChoiceItem();
  item20.setTitle('20. In STH control programs, what is the minimum coverage required for mass drug administration to be effective?')
    .setChoices([
      item20.createChoice('50%', false),
      item20.createChoice('65%', false),
      item20.createChoice('75%', true),
      item20.createChoice('90%', false)
    ])
    .setPoints(1);
  item20.setRequired(true);

  Logger.log('STH Quiz created successfully. URL: ' + form.getPublishedUrl());

  Logger.log('STH Quiz created successfully. URL: ' + form.getPublishedUrl());
}

// Function to add instructions page
function addInstructionsPage() {
  var form = FormApp.getActiveForm();
  var pageBreakItem1 = form.addPageBreakItem().setTitle('Instructions');
  var textItem = form.addSectionHeaderItem();
  textItem.setTitle('Instructions for the STH Quiz')
    .setHelpText('This quiz contains 20 multiple choice questions testing your knowledge of Soil Transmitted Diseases. Each question carries 1 mark. Good luck!');
}
