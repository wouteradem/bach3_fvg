<?php

$fi_Ek = array();
for ($i = 0; $i < 10; $i++) {
  $fi_Ek[$i] = array();
  for ($j = 0; $j < 10; $j++) {
    if (($handle = fopen("../data/EL_". $i . "_" . $j . ".csv", "r")) !== FALSE) {
      $line_index = 0;
      while (($data = fgets($handle)) !== FALSE) {
        $fi_Ek[$i][$line_index] += $data;
        $line_index++;
      }
      fclose($handle);
    }
  }  
}

var_dump($fi_Ek);
