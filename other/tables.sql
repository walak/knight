CREATE TABLE `result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descriptor` varchar(49) NOT NULL,
  `knight_start_x` int(11) NOT NULL,
  `knight_start_y` int(11) NOT NULL,
  `moves_number` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQUE_RESULT` (`descriptor`,`knight_start_x`,`knight_start_y`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
