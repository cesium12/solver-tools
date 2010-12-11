#!/usr/bin/ruby
require 'puz'

FACTORY = Crossword.new

# Augment the Crossword class with methods that extract answer words
class Crossword
    def get_word_across(row, col)
        str = ''
        square = @squares[col][row]
        until square.nil?
            str += square.answer
            col += 1
            break if col >= @width
            square = @squares[col][row]
        end
        return str
    end

    def get_word_down(row, col)
        str = ''
        square = @squares[col][row]
        until square.nil?
            str += square.answer
            row += 1
            square = @squares[col][row]
        end
        return str
    end
end

def get_clues(filename)
    clues = []
    crossword = FACTORY.parse(File.open(filename))
    0.upto(crossword.height - 1) do |row|
        0.upto(crossword.width - 1) do |col|
            square = crossword.squares[col][row]
            next if square.nil?
            if square.across
                text = crossword.get_word_across(row, col)
                clue = crossword.across[square.across]
                clues << [text, clue]
                puts text+"\t"+clue
            end
            if square.down
                text = crossword.get_word_down(row, col)
                clue = crossword.down[square.down]
                clues << [text, clue]
                puts text+"\t"+clue
            end
        end
    end
    return clues
end

def extract_clues(path)
    outname = path.sub('puzzles', 'clues').sub('.puz', '.txt')
    outfile = File.open(outname, "w")
    clues = get_clues(path)
    clues.each do |entry|
        text, clue = entry
        outfile.write(text+"\t"+clue+"\n")
    end
    outfile.close
end

def extract_clues_dir(dir)
    Dir.entries(dir).each do |filename|
        if filename =~ /\.puz$/
            path = File.join(dir, filename)
            extract_clues(path)
        end
    end
end

extract_clues_dir(ARGV[0])
