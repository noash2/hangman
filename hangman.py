import hangman_helper


def update_word_pattern(word, pattern, letter):
    """
    this function check if the letter is in the word or not. if it is, it
    adds her to the pattern
    """
    new_pattern = ""
    # new_pattern is the original pattern with the correct letters that were
    # guessed
    for i in range(len(pattern)):
        if pattern[i] == "_":
            if word[i] == letter:
                new_pattern = new_pattern + letter
            else:
                new_pattern = new_pattern + pattern[i]
        else:
            new_pattern = new_pattern + pattern[i]
    return new_pattern


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    this function builds the list of the possible words that fits to the
    pattern
    """
    hint_lst = []
    for i in range(len(words)):
        flag = True
        # flag is a parameter that indicates the condition to be true or false
        if len(words[i]) == len(pattern):
            for j in range(len(words[i])):
                if words[i][j] in wrong_guess_lst:
                    flag = False
                    break
                if pattern[j] != "_":
                    count_letter = pattern.count(pattern[j])
                    if words[i][j] == pattern[j] and count_letter == words[
                        i].count(words[i][j]):
                        continue
                    else:
                        flag = False
        else:
            continue
        if flag:
            hint_lst.append(words[i])
    return hint_lst


def run_single_game(words_list, score):
    """
    this function defines the process of 1 round in the game
    """
    word = hangman_helper.get_random_word(words_list)
    # print(word)
    pattern = "_" * len(word)
    wrong_guess_lst = []
    points = score
    msg = "Lets start playing"
    while points > 0 and "_" in pattern:
        hangman_helper.display_state(pattern, wrong_guess_lst, points, msg)
        (type_of_choice, choice) = hangman_helper.get_input()
        if type_of_choice == hangman_helper.LETTER:
            if len(choice) > 1 or not choice.islower():
                msg = "Your input is invalid, please try again"
            elif choice in wrong_guess_lst or choice in pattern:
                msg = "You chose this letter before, please try again"
            elif choice not in word:
                wrong_guess_lst.append(choice)
                points = points - 1
                msg = "This letter is not in the word, you've lost 1 point"
            elif choice in word:
                pattern = update_word_pattern(word, pattern, choice)
                # num is the number of times that the letter is in the word
                num = pattern.count(choice)
                points = points - 1
                points = points + ((num*(num+1))//2)
                msg = "Nice guess!"
        if type_of_choice == hangman_helper.WORD:
            points = points - 1
            if choice == word:
                # count is the number of letters that are not _
                count = 0
                for i in pattern:
                    if i == "_":
                        count += 1
                pattern = word
                points = points + ((count*(count+1))//2)
                break
            elif choice != word:
                msg = "Wrong guess, please try again"
        hint_lst = filter_words_list(words_list, pattern, wrong_guess_lst)
        lst_2 = []
        if type_of_choice == hangman_helper.HINT:
            points = points - 1
            if len(hint_lst) > hangman_helper.HINT_LENGTH:
                for i in range(hangman_helper.HINT_LENGTH):
                    idx = i*len(hint_lst)//hangman_helper.HINT_LENGTH
                    lst_2.append(hint_lst[idx])
                hint_lst = lst_2
            msg = " "
            hangman_helper.show_suggestions(hint_lst)
    if points == 0:
        msg = "You lost the game, the word was: " + word
    if pattern == word:
        msg = "Congratulations! You won the game"
    hangman_helper.display_state(pattern, wrong_guess_lst, points, msg)
    return points


def main():
    """
    this function defines the whole game that includes few rounds or 1
    round- according to the player's choice
    """
    word_list = hangman_helper.load_words()
    points = run_single_game(word_list, hangman_helper.POINTS_INITIAL)
    games_num = 0
    msg = ""
    while True:
        if points > 0:
            games_num += 1
            msg = "Do you want to play another game? So far you have played " \
                  "" + str(games_num) + " games. You have " + str(points) \
                  + " points"
            play = hangman_helper.play_again(msg)
            if play:
                points = run_single_game(word_list, points)
            else:
                break
        elif points == 0:
            points = hangman_helper.POINTS_INITIAL
            games_num += 1
            msg = "Do you want to play another game? So far you have played " \
                  "" + str(games_num) +" games"
            games_num = 0
            play = hangman_helper.play_again(msg)
            if play:
                points = run_single_game(word_list, points)
            else:
                break
        else:
            break


if __name__ == '__main__':
    main()
