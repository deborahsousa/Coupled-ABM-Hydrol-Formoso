/**
* Name: FRBModel 
* Authors: Déborah S. Sousa, Cássio G. C. Coelho, Conceição de M. A. Alves, Célia G. Ralha.
* Tags: irrigation; water regulation
* The 'cycle > 1' conditions ensure that the simulation starts in the correct day (1st May)
*/
model UrubuRiverModel

global {
	//INPUTS
	//Files: matrices and shapefiles
	file shapefile_pumps <- file("../includes/urubu_pumps.shp"); //irrigation pumps from GAN
	matrix farmers_data <- file("../includes/urubu_farmers.csv"); //Farmer agents information
	list<string> daily_date <- file("../includes/daily_date.txt");
	matrix<float> prob_CI <- file("../includes/CI-prob.csv");
	matrix<float> prob_NC <- file("../includes/NC-prob.csv");
	matrix<float> prob_CP <- file("../includes/CP-prob.csv");
	matrix<float> limits_withdrawal <- file("../includes/limits-withdrawal.csv");
	matrix level_series <- file("../includes/level_reference_gauge.csv");
	file shapefile_hidro <- file("../includes/streamwork.shp"); //irrigation channels from SEMARH	
	file shapefile_channels <- file("../includes/irrigation_channels.shp"); //irrigation channels from SEMARH
	file shapefile_land <- file("../includes/area_urubu.shp"); // agricultural properties in the Urubu river basin
	//geometry shape <- envelope(shapefile_land);
	
	//Biennium Plan rules
	float yellow_level <- 398; // centimeters
	float red_level <- 220; // centimeters
	date attention_date <- date("2020-07-01");
	date restriction_date <- date("2020-08-01");
	int col_level;
	float current_level <- 500 update:level_series[col_level,cycle];//level variation at the reference gauging station [cm] //might be given as an input of a hydrological model output
	bool aux_level_red update:(current_level <= red_level);
	bool aux_level_yellow update:(current_level <= yellow_level);
	bool aux_date_08 update:(current_date >= restriction_date);
	bool aux_date_07 update:(current_date >= attention_date);
	date my_day <- starting_date update: update_my_date();
		
	//counters and time steps (dry season)
	date starting_date <- date("2020-05-01");
	float step <- 1 #day;
	int nb_days <- 123; //day count from the first to the last day of one dry season simulation
	string crop_season <- "soybean" among: ["soybean","rice"];
	int twoweeks_count update:update_twoweeks_count();	
	int day_in_twoweeks  update: update_day_in_twoweeks();

	action update_my_date type: date { //adjusts the date to save it correctly in the output file
		if cycle > 0 {
			date my_new_date <- daily_date[cycle]; 
			return my_new_date;
		} else {
			return starting_date;
		} 
	}

	action update_day_in_twoweeks type: int {
		if mod(cycle,15) != 0 or (cycle) >= 120 {
			return day_in_twoweeks + 1;
		} else {
			return 0;
		} 
	}
	
	action update_twoweeks_count type: int {
		if cycle = 0{
			return 0;
		}else if ((cycle) < 120) {
			return floor((cycle)/15);
		}else if ((cycle) >= 120) {
			return 7;
		}
	}
			
	//SCENARIOS
	//string scenario;
	//string scenario <- "S4"; //baseline + average level
	//string scenario <- "S4-max" ;//baseline + max level
	//string scenario <- "S4-min"; //baseline + min level
	//string scenario <- "S5" ;//all CP with bdi and baseline level
	//string scenario <- "S6";//all CP with bdi and max level
	//string scenario <- "S7";//all CP with bdi and min level
	//string scenario <- "S8"; //all CI	with bdi and baseline level
	//string scenario <- "S9";//all CI with bdi and min level
	//string scenario <- "S10";//all CI with bdi and max level
	//string scenario <- "S11";//all NC with bdi and min level
	//string scenario <- "S12"; //baseline + average level + neighbourhood apenas CI
	//string scenario <- "S13"; //swap CP and NC + average level + neighbourhood apenas CI
	//string scenario <- "S14"; //CP-NC swaped in D1 + + rest is the same + average level 
	string scenario <- "S15"; //CP-NC swaped in D2 + rest is the same + average level 
	
	//Demand group effect
	float n_CP; //fraction of CP farmers in a demand_g
	float n_CI; //fraction of CI farmers in a demand_g
	float n_NC; //fraction of NC farmers in a demand_g
	
	//COLLECTIVE VARIABLES IN OUTPUT	
	list<float> all_pumps_daily_withdrawal update: Pump collect (each.daily_withdrawal);

/***********
initial state****************/
	init {
		/*//loading parameters for scenarios simulation
		create Land from: shapefile_land;
		create Channel from: shapefile_channels;
		create Hidro from: shapefile_hidro;*/
		
		//creating the Pump agent
		create Pump from: shapefile_pumps;
		list<int> farmer_id_list <- Pump collect each.f_id;
		list<int> farmer_id_list <- remove_duplicates(Pump collect each.f_id);
		list<int> pump_id_list <- Pump collect each.p_id;
		
		//creating the Farmer agent
		create Farmer number: length(farmer_id_list);
		int i <- 0;
		loop farmer over: Farmer {
			farmer.f_id <- farmer_id_list[i];
			i <- i + 1;
		}
		
		//creating the Regulator agent
		create Regulator;

		//relate farmers to profiles, demand group and area
		loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
			loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
				int my_farmer_data_id <- int(farmers_data[0,i]);
				if Farmer[j].f_id = my_farmer_data_id{
					Farmer[j].irrigation_area <- farmers_data[5,i]; 
					Farmer[j].demand_g <- farmers_data[3,i];
					Farmer[j].nb_pumps <- length(Farmer[j].owned_pumps); // number of owned pumps	
				}
			}
		}	
		
		//Scenarios settings
		switch scenario {
			match 'S4'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].f_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}
				col_level <- 1;
			}		
			
			match 'S4-max'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].f_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}
				col_level <- 2;
			}		
			
			match 'S4-min'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].f_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}
				col_level <- 3;
			}			

			match 'S5'{
				loop farmer over:Farmer {
					farmer.profile <- 'CP';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CP';
				} 
				col_level <- 1;
			}
			
			match 'S6'{
				loop farmer over:Farmer {
					farmer.profile <- 'CP';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CP';
				} 
				col_level <- 2;
			}
			
			match 'S7'{
				loop farmer over:Farmer {
					farmer.profile <- 'CP';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CP';
				} 
				col_level <- 3;
			}
			
			match 'S8'{
				loop farmer over:Farmer {
					farmer.profile <- 'CI';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CI';
				} 
				col_level <- 1;
			}
			
			match 'S9'{
				loop farmer over:Farmer {
					farmer.profile <- 'CI';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CI';
				} 
				col_level <- 2;
			}
			
			match 'S10'{
				loop farmer over:Farmer {
					farmer.profile <- 'CI';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'CI';
				} 
				col_level <- 3;
			}
			
			match 'S11'{
				loop farmer over:Farmer {
					farmer.profile <- 'NC';
				}
				
				loop pump over:Pump {
					pump.f_profile <- 'NC';
				} 
				col_level <- 1;
			}
			
			match 'S12'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].f_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}					
				col_level <- 1;
			}
			
			match 'S13'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].f_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}
				
				loop farmer over:Farmer {
					if farmer.profile = 'CP'{
						farmer.profile <- 'NC';
					}else if farmer.profile = 'NC'{
						farmer.profile <- 'CP';
					}	
				}
				
				loop pump over:Pump {
					if pump.f_profile = 'NC'{
						pump.f_profile <- 'CP';
					}else if pump.f_profile = 'CP'{
						pump.f_profile <- 'NC';
					}
				} 
					
				col_level <- 1;
			}
			
			match 'S14'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].f_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}
				
				loop farmer over:Farmer {
					if farmer.profile = 'CP' and farmer.demand_g = 'D1'{
						farmer.profile <- 'NC';
					}else if farmer.profile = 'NC' and farmer.demand_g = 'D1'{
						farmer.profile <- 'CP';
					}	
				}
				
				loop pump over:Pump {
					if pump.f_profile = 'NC' and pump.demand_g = 'D1'{
						pump.f_profile <- 'CP';
					}else if pump.f_profile = 'CP' and pump.demand_g = 'D1'{
						pump.f_profile <- 'NC';
					}
				} 
					
				col_level <- 1;
			}
			
			match 'S15'{
				loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
					loop i from: 0 to: length(farmer_id_list) - 1 step: 1{
						int my_farmer_data_id <- int(farmers_data[0,i]);
						if Farmer[j].f_id = my_farmer_data_id{
							Farmer[j].profile <- farmers_data[2,i];
						}
					}
				}
				
				loop farmer over:Farmer {
					if farmer.profile = 'CP' and farmer.demand_g = 'D2'{
						farmer.profile <- 'NC';
					}else if farmer.profile = 'NC' and farmer.demand_g = 'D2'{
						farmer.profile <- 'CP';
					}	
				}
				
				loop pump over:Pump {
					if pump.f_profile = 'NC' and pump.demand_g = 'D2' {
						pump.f_profile <- 'CP';
					}else if pump.f_profile = 'CP' and pump.demand_g = 'D2'{
						pump.f_profile <- 'NC';
					}
				} 
					
				col_level <- 1;
			}
		}			
		
		//relate pumps to farmers 
		loop i from: 0 to: length(pump_id_list) - 1 step: 1 {
			loop j from: 0 to: length(farmer_id_list) - 1 step: 1 {
				if Pump[i].f_id = Farmer[j].f_id {
					add Pump[i] to: Farmer[j].owned_pumps;
					Pump[i].pump_owner <- Farmer[j];
					Pump[i].irrigation_area <- Farmer[j].irrigation_area;
				}
			}
		}
		
		list<Farmer> mygroup1 <- Farmer where (each.demand_g = 'D1');
		list<Farmer> mygroup2 <- Farmer where (each.demand_g = 'D2');
		list<Farmer> mygroup3 <- Farmer where (each.demand_g = 'D3');
		
		//assign farmers' peers according to demand group
		ask Farmer {
			if demand_g = 'D1'{
				my_group <- mygroup1;
			}else if demand_g = 'D2'{
				my_group <- mygroup2;
			}else if demand_g = 'D3'{
				my_group <- mygroup3;
			}
			n_CP <- length(my_group where (each.profile = 'CP'))/length(my_group);
			n_NC <- length(my_group where (each.profile = 'NC'))/length(my_group);
		}
		
		// assign pump' probability matrix according to profile
		ask Pump {
			if f_profile = 'CP'{
				prob_matrix <- prob_CP;
			}else if f_profile = 'NC'{
				prob_matrix <- prob_NC;
			}else if f_profile = 'CI'{
				prob_matrix <- prob_CI;
			}
		}
							
	}/******END INIT*****/		
			
	reflex save_daily_data when: cycle > 0{	
		save [cycle,int(self),my_day,all_pumps_daily_withdrawal] to: "../results/scenarios-bdi/daily_withdrawal"+scenario+".csv"  type:csv rewrite:false header:false;				 
		//string day_of_the_year <- daily_date[cycle-1];
		//write 'ciclo '+cycle+' '+day_of_the_year+' '+' '+all_pumps_daily_withdrawal;
		//list<float> all_pumps_daily_withdrawal <- Pump collect (each.daily_withdrawal);	
		//save [cycle,int(self),day_of_the_year,all_pumps_daily_withdrawal]to: "../results/exemplo1.csv"  type:csv rewrite:false header:false;				
		//save [cycle,int(self),day_of_the_year,f_daily_withdrawal]to: "../results/daily_withdrawal-farmer-100.csv"  type:csv rewrite:false;
		//save [cycle,int(self),day_of_the_year,all_pumps_daily_withdrawal]to: "../results/daily_withdrawal-pumps-1000-keepseed"+scenario+"-init0.csv"  type:csv rewrite:false;
	}
	
	reflex end_simulation when:cycle=nb_days+1{
		do pause;
	}
}/******END GLOBAL*****/

species Pump {
	Pump pump;
	int p_id; // pump identification number
	string rotulo; // pump identification. Source: GAN (2022).
	int f_id; //farmer owner identification number
	matrix prob_matrix;
	list<float> p_list;
	Farmer pump_owner; //pump owner/farmer agent identification number
	string f_profile; //behaviour group of the pump's owner (cooperative profile)
	string demand_g; //demand group of the pump's owner. Source: Volken (2022).
	float irrigation_area; // irrigation area of the land property. Source: GAN (2022).
	int size <- 150;
	rgb color <- #black;
	float daily_withdrawal update:update_withdrawal(cycle);

	aspect default {
		draw circle(size) color:color border: #black;
	}
	
	action update_withdrawal (int cycle){
		list<float> p_list <- column_at(prob_matrix,twoweeks_count);
		int interval_index <- rnd_choice(p_list);
		float a <- limits_withdrawal[0,interval_index];
		float b <- limits_withdrawal[1,interval_index];
		daily_withdrawal <- rnd(a,b);
		ask pump_owner {
			if has_belief(trigger_restriction_rule){
				return 0.0; //stops withdrawal completely
			}else if has_belief(trigger_attention_rule){
				return 0.5*myself.daily_withdrawal; //50% reduction
			}else{
				return myself.daily_withdrawal;
			}
		}
	}
}

species Farmer control: simple_bdi {
	Farmer farmer;
	int f_id;
	string profile;
	string demand_g;
	list<Pump> owned_pumps; // list of owned pumps 
	list<Farmer> my_group;
	int nb_pumps;
	float irrigation_area; //potential irrigation area [ha]
	float f_daily_withdrawal update: update_f_withdrawal();
	rgb color <- #grey;
	float n_NC;
	float n_CP;
	
	predicate trigger_attention_rule <- new_predicate("Attention rule must be obeyed");
	predicate trigger_restriction_rule <- new_predicate("Restriction rule must be obeyed");
	predicate obey_restriction_rule <- new_predicate("I am obeying the restriction rule");
	predicate most_NC <- new_predicate('Most are NC in my group');
	predicate most_CP <- new_predicate('Most are CP in my group');
	
	/*aspect default {
		draw circle(150) color: color border: #black;
	}*/

	action update_f_withdrawal {
		return sum(collect(owned_pumps,each.daily_withdrawal));
	}
	
	//Neighbourhood effect
	reflex my_neighbours {
		if n_NC > n_CP {
			do add_belief(most_NC);
		}else if n_CP > n_NC {
			do add_belief(most_CP);
		}
	}
		
	reflex neigh_effect{	
		if scenario = 'S12' or scenario = 'S13' or scenario = 'S14' or scenario = 'S15'{
			if profile = 'CI' {
				if has_belief(most_NC){
					profile <- "NC";
					ask owned_pumps{
						prob_matrix <- prob_NC;
						f_profile <- "NC";
					}
				}else if has_belief(most_CP){
					profile <- "CP";
					ask owned_pumps{
						prob_matrix <- prob_CP;
						f_profile <- "CP";
					}
				}
			}
		}
	}
	
	reflex assign_beliefs {
		if(profile = "CP"){
			if((aux_date_08) or (aux_level_red)){
				do add_belief(trigger_restriction_rule);
			}else if((aux_date_07) or (aux_level_yellow)){
				do add_belief(trigger_attention_rule);
			}
		}else if (profile = 'CI'){
			if((aux_date_08) and (aux_level_red)){
				do add_belief(trigger_restriction_rule);
			}else if((aux_date_07) and (aux_level_yellow)){
				do add_belief(trigger_attention_rule);
			}
		}
	}
	
	rule belief: trigger_restriction_rule new_desire: obey_restriction_rule;
	//rule belief: trigger_attention_rule new_desire: obey_attention_rule;	
	
	reflex assign_colours{
		bool is_respecting_red_rules <- false;
		bool is_respecting_yellow_rules <- false;
		
		if ((aux_date_08) or (aux_level_red)) {
			if f_daily_withdrawal = 0 {
				is_respecting_red_rules <- true;
			}else if f_daily_withdrawal > 0 {
				is_respecting_red_rules <- false;
			}
		}
		
		if (!(aux_date_08) and !(aux_level_red)){
			is_respecting_red_rules <- true;
		}

		if (!(aux_date_07) and !(aux_level_yellow)){
			is_respecting_yellow_rules <- true;
		}
		
		if (!is_respecting_red_rules or !is_respecting_yellow_rules){
			loop pump over: owned_pumps {
				pump.color <- #red;
				pump.size <- 200;
			}
		}else{
			loop pump over: owned_pumps {
				pump.color <- #black;
				pump.size <- 150;
			}
		}
	}
}

species Regulator control:simple_bdi{
	date fiscalization_date1 <- attention_date;
	date fiscalization_date2 <- restriction_date;
	predicate restriction_rule <- new_predicate('restriction_rule');
	predicate attention_rule <- new_predicate('attention_rule');
	
	reflex regulate {
		if((aux_date_08) or (aux_level_red)) { 
			do add_belief(restriction_rule);
		}else if((aux_date_07) or (aux_level_yellow)) {
			do add_belief(attention_rule);
		}
	}
}

// Auxiliar species for GUI experiments
species Land {

	aspect default {
		draw shape color: #darkgreen border: #black;
	}
}

species Channel {

	aspect default {
		draw shape color: #black border: #black;
	}
}

species Hidro {

	aspect default {
		draw shape color: #blue border: #black;
	}
}	

experiment teste_gui type: gui {
	output {
		/*display map refresh: every(1 #cycle) {
			species Hidro;
			species Channel;
			species Land;
			species Pump;
			species Farmer;
		}*/

		display Irrigation_per_pump refresh: every(1 #cycle) {
			chart "Individual water consumption (m³)" type: series x_serie_labels:my_day{
				datalist Pump collect (each.rotulo) value: Pump collect (each.daily_withdrawal) style: line ;
			}
		}

		display Irrigation_per_farmer refresh: every(1 #cycle) {
			chart "Total water consumption (m³)" type: series  x_serie_labels:my_day{
				datalist Farmer collect string(each.f_id) value: Farmer collect sum (each.owned_pumps collect each.daily_withdrawal) style: line;
			}
		}
		
		display Irrigation_total refresh: every(1 #cycle) {
			chart "Total water consumption (m³)" type: series x_serie_labels:my_day{
				data "All pumps" value: sum((Pump collect (each.daily_withdrawal))) style: line color: #black;
			}
		}

		display Irrigation_total_pump_profile refresh: every(1 #cycle) {
			chart "Water consumption (m³) per profile" type: series x_serie_labels:my_day{
				data "CP" value: sum((Pump where (each.f_profile = "CP")) collect (each.daily_withdrawal)) style: line color: #magenta;
				data "CI" value: sum((Pump where (each.f_profile = "CI")) collect (each.daily_withdrawal)) style: line color: #cyan;
				data "NC" value: sum((Pump where (each.f_profile = "NC")) collect (each.daily_withdrawal)) style: line color: #yellow;
			}
		}
		
		display Irrigation_total_pump_group refresh: every(1 #cycle) {
			chart "Water consumption (m³) per profile" type: series x_serie_labels:my_day{
				data "D1" value: sum((Pump where (each.demand_g = "D1")) collect (each.daily_withdrawal)) style: line color: #magenta;
				data "D2" value: sum((Pump where (each.demand_g = "D2")) collect (each.daily_withdrawal)) style: line color: #cyan;
				data "D3" value: sum((Pump where (each.demand_g = "D3")) collect (each.daily_withdrawal)) style: line color: #yellow;
			}
		}
		
		/*display AverageIrrigation_total_pump_profile refresh: every(1 #cycle) {
			chart "Average water consumption (m³) per pump per profile" type: series {
				data "CP" value: sum((Pump where (each.f_profile = "CP")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "CP")) color: #magenta;
				data "CI" value: sum((Pump where (each.f_profile = "CI")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "CI"))  color: #cyan;
				data "NC" value: sum((Pump where (each.f_profile = "NC")) collect (each.daily_withdrawal))*length(Pump)/length(Pump where(each.f_profile = "NC"))  color: #yellow;
			}
		}*/
	}
}

experiment repetitions type: batch repeat: 1000 autorun: true keep_seed:true until: cycle = nb_days+1 { 	
	reflex end_of_runs {
		int sim <- 0;
		ask simulations { // at the end of the simulation, for each simulation
			sim <- sim + 1;	
		}
	}
} 